from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Restaurant
from django.shortcuts import HttpResponseRedirect,Http404,HttpResponse,render_to_response,get_object_or_404,get_list_or_404
from django.db import models, connection
import json
from django.core import serializers
from django.http import JsonResponse
from dish import models as dish_models
from serves import models as serves_models
from likes import models as likes_models
from visits import models as visits_models
from django.db.models import Max
import numpy as np

# Create your views here.
# def home(request):
#     return render(request,'restaurant/home.html')
# def home(request):

#     result = get_list_or_404(Restaurant)  
#     # results = Restaurant.objects.raw('SELECT * FROM "restaurant_restaurant"')
#     # return render(request, 'index.html', {'results': results})
    
#     res = Restaurant.objects.all()
#     results = serializers.serialize('json', res)

#     # print(results)
#     # print(type(results))
#     return render(request, 'index.html', {'results': res, 'r2' : results})

def home(request):
    restaurants = Restaurant.objects
    return render(request,'index.html',{'restaurants':restaurants})

@login_required
def create(request):
    if (request.method == 'POST'):
        if request.POST['rname'] and request.POST['cuisine']  and request.POST['url'] and request.POST['phone']:

            restaurant = Restaurant()
            restaurant.name = request.POST['rname']
            restaurant.cuisine = request.POST['cuisine']
            restaurant.location = "location"
            restaurant.likes = 1
            restaurant.url = request.POST['url']
            restaurant.lat = request.POST['lat']
            restaurant.lng = request.POST['lng']
            restaurant.phone = request.POST['phone']
            if request.FILES.get('img') is not None:
                restaurant.photo = request.FILES.get('img')
            restaurant.is_veg = True if request.POST.get('vegc') is not None else False
            restaurant.is_nightlife = True if request.POST.get('nightc') is not None else False
            restaurant.is_finedining = True if request.POST.get('finec') is not None else False
            restaurant.is_dessert = True if request.POST.get('dessertc') is not None else False
            restaurant.is_cafe = True if request.POST.get('cafec') is not None else False
            restaurant.save()
            # print()
            
            # c = connection.cursor()
            # c.execute("INSERT INTO restaurant_restaurant (name, cuisine, url, location, likes, lat, lng, photo, phone) VALUES ( ' " 
            #     + request.POST['rname'] + " ' , ' "  
            #     + request.POST['cuisine'] + " ' , ' "
            #     + request.POST['url'] + " ' , ' "
            #     + ' ' + " ' , ' "
            #     + str(1) + " ' , ' "
            #     + str(request.POST['lat']) + " ' , ' "
            #     + str(request.POST['lng']) + " ' , ' "
            #     + request.FILES.get('img') + " ' , ' "
            #     + request.POST['phone']  + " ' ) "
            #     )
            results = Restaurant.objects.raw('SELECT id FROM "restaurant_restaurant"')
            print(results[:-1])
            connection.commit()
            # return redirect('/restaurant/'+ str(results[-1].id))
            results = Restaurant.objects.raw('SELECT * FROM "restaurant_restaurant"')
            # return render(request, 'index.html', {'results': results})
            return redirect('/restaurant/' + str(restaurant.id))
        else:
            return render(request,'restaurant/create.html',{'error':'All fields required'})
    else:
        return render(request,'restaurant/create.html')


def detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
    serves = serves_models.Serves.objects.filter(restaurant_id=restaurant_id)
    user = request.user
    try:
        visit_obj = visits_models.Visits.objects.get(rest_id=restaurant,user_id=user)
        visit_obj.count += 1
        visit_obj.save()
    except:
        visit_obj = visits_models.Visits()
        visit_obj.rest_id = restaurant
        visit_obj.user_id = user
        visit_obj.save()
    return render(request, 'restaurant/detail.html',context={'restaurant':restaurant,'serves':serves})

@login_required
def like(request, restaurant_id):
    if (request.method == 'POST'):
        restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
        restaurant.num_likes = restaurant.num_likes + 1
        restaurant.save()
        # c = connection.cursor()
        # c.execute('SELECT num_likes FROM "restaurant_restaurant" WHERE id = ' + str(restaurant_id))
        # count = c.fetchall()
        # mydata = c.execute('UPDATE restaurant_restaurant SET num_likes = '+ str(count[0][0] + 1) +' WHERE id = ' + str(restaurant_id))
        # connection.commit()
        user = request.user
        try:
            like_obj = likes_models.Likes.objects.get(rest_id=restaurant,user_id=user)
            like_obj.count += 1
            like_obj.save()
        except:
            like_obj = likes_models.Likes()
            like_obj.rest_id = restaurant
            like_obj.user_id = user
            like_obj.save()
        return redirect('/restaurant/'+ str(restaurant_id))


@login_required
def delete(request, restaurant_id):
    if (request.method == 'POST'):
        restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
        restaurant.delete()
        #return render(request, 'restaurant/home.html')
        restaurants = Restaurant.objects
        return render(request,'restaurant/home.html',{'restaurants':restaurants})


@login_required
def search(request):
    query = request.GET['searchbar'].lower()
    min = request.GET['amount_min']
    max = request.GET['amount_max']
    likes = request.GET.get('likes_number')
    if likes == "option1":
        print("larger than 50")
        likes = 50
    elif likes == "option2":
        likes = 100
        print("larger than 100")
    elif likes == "option3":
        likes = 150
        print("larger than 150")
    else:
        likes = 0
        print("likes is not limited")

    isVeg = True if request.GET.get('veg') is not None else False
    isNight = True if request.GET.get('night') is not None else False
    isFine = True if request.GET.get('fine') is not None else False
    isDessert = True if request.GET.get('dessert') is not None else False
    isCafe = True if request.GET.get('cafe') is not None else False

    # query = request.GET['searchbar']
    # q1 = query.split(':')
    # name = q1[0]
    # dPrice = q1[1]
    # min = int(float(dPrice )) - 3
    # max = int(float(dPrice ))+ 3
    # serve = serves_models.Serves.objects.filter(dname=name,price__range=(min,max)).values_list('restaurant_id_id', flat=True)
    # restaurants = Restaurant.objects.filter(pk__in=serve)
    # return render(request,'restaurant/search.html',{'restaurants':restaurants})
    category_query = ""
    if isVeg:
        category_query += " AND r.is_veg "
    if isDessert:
        category_query +=  " AND r.is_dessert "
    if isFine:
        category_query +=  " AND r.is_finedining "
    if isNight:
        category_query +=  " AND r.is_nightlife "
    if isCafe:
        category_query +=  " AND r.is_cafe "

    if request.GET.get('searchby') is None or  request.GET.get('searchby') == "restaurant":

        #search resturant
        c = connection.cursor()
        c.execute(
            "SELECT r.name FROM restaurant_restaurant AS r \
            LEFT JOIN serves_serves AS s ON r.id = s.restaurant_id_id \
            WHERE (LOWER(r.name) LIKE LOWER(%s) OR r.cuisine LIKE %s OR r.location LIKE %s OR LOWER(s.dname) LIKE LOWER(%s) )"
            + category_query +
            "GROUP BY r.name HAVING MIN(s.price) >= " + min + " AND MAX(s.price) <= "+ max +"AND SUM(s.likes) >= " + str(likes)
            , ['%'+request.GET['searchbar']+'%','%'+request.GET['searchbar']+'%','%'+request.GET['searchbar']+'%','%'+request.GET['searchbar']+'%'])

        restaurants = c.fetchall()
        # restaurants.filter()
        print("restaurant", restaurants)
        print("type", type(restaurants))
        ids = []
        for r in restaurants:
            id = Restaurant.objects.filter(name=r[0])
            ids.append(id)
            print("id", id)
        num = len(ids)
        return render(request,'restaurant/search.html',{'search_results':restaurants, 'ids': ids, 'num': num})
        
    else:
       # seearch dises
        c_dish = connection.cursor()
        c_dish.execute(
            "SELECT s.dname, r.id FROM restaurant_restaurant AS r \
            LEFT JOIN serves_serves AS s ON r.id = s.restaurant_id_id \
            WHERE LOWER(s.dname) LIKE LOWER(%s)\
            AND s.price >= " + min + " AND s.price <= "+ max +" \
            AND s.likes >= " + str(likes) + " \
            " + category_query
            , ['%'+request.GET['searchbar']+'%'])
        dishes = c_dish.fetchall()
        result = []
        for dish in dishes:
            d = {}
            d['name'] = dish[0]
            d['id'] = dish[1]
            result.append(d)
        # ids = []
        # for r in restaurants:
        #     id = Restaurant.objects.filter(name=r[0])
        #     ids.append(id)
        #     print("id", id)

        return render(request,'restaurant/search.html',{'dishes': result})


@login_required
def add_dish(request, restaurant_id):
    if (request.method == 'POST'):
        if request.POST['dname'] and request.POST['price']:
            dish = dish_models.Dish()
            dish.name = request.POST['dname']
            dish.save()
            serves = serves_models.Serves()
            serves.dname = request.POST['dname']
            serves.restaurant_id = Restaurant.objects.get(pk=restaurant_id)
            serves.is_speciality = False
            serves.is_veg = False
            serves.price =  request.POST['price']
            serves.save()
            restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
            restaurants = Restaurant.objects
            return redirect('/restaurant/'+ str(restaurant_id))


@login_required
def like_dish(request, restaurant_id, serve_id):
    restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
    serve = get_object_or_404(serves_models.Serves, pk = serve_id)
    serve.likes += 1
    serve.save()
    return redirect('/restaurant/'+ str(restaurant.id))

@login_required
def statistics(request):
    if (request.method == 'GET'):
        return render(request,'restaurant/statistics.html')


def recommend(request):
    user = request.user
    rest_list_1 = likes_models.Likes.objects.filter(user_id=user.id).values_list('rest_id')
    cuisines_1 = Restaurant.objects.filter(pk__in=rest_list_1).values_list('cuisine')
    rest_list_2 = visits_models.Visits.objects.filter(user_id=user.id).values_list('rest_id')
    cuisines_2 = Restaurant.objects.filter(pk__in=rest_list_2).values_list('cuisine')
    cuisines = cuisines_1.union(cuisines_2)
    exclude_rests = rest_list_1.union(rest_list_2)
    restaurants = Restaurant.objects.filter(cuisine__in=cuisines).exclude(pk__in=exclude_rests)

    rests_1 = Restaurant.objects.filter(pk__in=rest_list_1)
    rests_2 = Restaurant.objects.filter(pk__in=rest_list_2)
    rests = list(rests_1.union(rests_2))

    #restaurants = rests_1.union(rests_2)

    recommend_dict = {"is_veg" : 0, "is_dessert" : 0, "is_nightlife" : 0, "is_finedining" : 0, "is_cafe" : 0}
    for i in rests:
        if i.is_veg == True:
            recommend_dict["is_veg"] += 1
        if i.is_dessert == True:
            recommend_dict["is_dessert"] += 1
        if i.is_nightlife == True:
            recommend_dict["is_nightlife"] += 1
        if i.is_finedining == True:
            recommend_dict["is_finedining"] += 1
        if i.is_cafe == True:
            recommend_dict["is_cafe"] += 1

    # sorted_dict = sorted(recommend_dict.items(), key=lambda kv: kv[1])
    # count = 0
    # ret = []
    ret = []
    key_1 = max(recommend_dict, key=recommend_dict.get)
    val_1 = recommend_dict[key_1]
    del(recommend_dict[key_1])
    if (val_1 == 0):
        key_1 = "empty"
    key_2 = max(recommend_dict, key=recommend_dict.get)

    if (recommend_dict[key_2] == 0):
        key_2 = "empty"



    container = Restaurant.objects.none()
    if key_1 == "is_veg":
        container = Restaurant.objects.filter(is_veg = True)
    if key_1 == "is_dessert":
        container = Restaurant.objects.filter(is_dessert = True)
    if key_1 == "is_nightlife":
        container = Restaurant.objects.filter(is_nightlife = True)
    if key_1 == "is_finedining":
        container = Restaurant.objects.filter(is_finedining = True)
    if key_1 == "is_cafe":
        container = Restaurant.objects.filter(is_cafe = True)

    container_2 = Restaurant.objects.none()
    if key_2 == "is_veg":
        container_2 = Restaurant.objects.filter(is_veg = True)
    if key_2 == "is_dessert":
        container_2 = Restaurant.objects.filter(is_dessert = True)
    if key_2 == "is_nightlife":
        container_2 = Restaurant.objects.filter(is_nightlife = True)
    if key_2 == "is_finedining":
        container_2 = Restaurant.objects.filter(is_finedining = True)
    if key_2 == "is_cafe":
        container_2 = Restaurant.objects.filter(is_cafe = True)

    restaurants = restaurants | (container & container_2)

    # user_liked = likes_models.Likes.objects.filter(user_id=user.id)
    # user_visited = visits_models.Visits.objects.filter(user_id=user.id)
    # most_liked = user_liked.filter('count'__max)
    # most_visited = user_visited.aggregate(Max('count'))
    # most_liked_rest = Restaurant.objects.get(pk=most_liked)
    # most_visited_rest = Restaurant.objects.get(pk=most_visited)

    # restaurants = restaurants | most_liked_rest

    recommend_dict_2 = {"is_veg" : 0, "is_dessert" : 0, "is_nightlife" : 0, "is_finedining" : 0, "is_cafe" : 0}
    for i in rests:
        if i.is_veg == True:
            recommend_dict_2["is_veg"] += 1
        if i.is_dessert == True:
            recommend_dict_2["is_dessert"] += 1
        if i.is_nightlife == True:
            recommend_dict_2["is_nightlife"] += 1
        if i.is_finedining == True:
            recommend_dict_2["is_finedining"] += 1
        if i.is_cafe == True:
            recommend_dict_2["is_cafe"] += 1

    user_vector = [0,0,0,0,0]
    user_vector[0] = recommend_dict_2["is_veg"]
    user_vector[1] = recommend_dict_2["is_dessert"]
    user_vector[2] = recommend_dict_2["is_nightlife"]
    user_vector[3] = recommend_dict_2["is_finedining"]
    user_vector[4] = recommend_dict_2["is_cafe"]
    if (user_vector == [0,0,0,0,0]):
        return render(request,'restaurant/recommend.html',{'restaurants':restaurants})
    user_vector = user_vector/(np.linalg.norm(user_vector))
    #iterate through all restaurants to create vector for each restaurant
    all_restaurants = Restaurant.objects.all()
    rest_dict = {}
    for r in all_restaurants:
        rest_dict[r] = 0
    for key in rest_dict.keys():
        r_vector = [key.is_veg,key.is_dessert,key.is_nightlife,key.is_finedining,key.is_cafe]
        rest_dict[key] = (np.dot(r_vector,user_vector))/(np.linalg.norm(user_vector)*np.linalg.norm(r_vector))

    key_3 = min(rest_dict, key=rest_dict.get)
    del(rest_dict[key_3])
    key_4 = min(rest_dict, key=rest_dict.get)

    query3 = Restaurant.objects.filter(pk=key_3.id)
    query4 = Restaurant.objects.filter(pk=key_4.id)

    restaurants = restaurants | query3 | query4

    if (restaurants.count() > 5):
        restaurants = restaurants.order_by('-num_likes')
        rest_list = (list(restaurants))[:5]
        rest_list_id = []
        for r in rest_list:
            rest_list_id.append(r.id)
        restaurants = Restaurant.objects.filter(pk__in = rest_list_id)

    return render(request,'restaurant/recommend.html',{'restaurants':restaurants})



