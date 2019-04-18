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
# Create your views here.
# def home(request):
#     return render(request,'restaurant/home.html')
def home(request):

    result = get_list_or_404(Restaurant)  
    # results = Restaurant.objects.raw('SELECT * FROM "restaurant_restaurant"')
    # return render(request, 'index.html', {'results': results})
    
    res = Restaurant.objects.all()
    results = serializers.serialize('json', res)

    # print(results)
    # print(type(results))
    return render(request, 'index.html', {'results': res, 'r2' : results})

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
            photo = request.FILES.get('img')
            restaurant.photo = photo
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
            return render(request, 'index.html', {'results': results})
        else:
            return render(request,'restaurant/create.html',{'error':'All fields required'})
    else:
        return render(request,'restaurant/create.html')


def detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
    serves = serves_models.Serves.objects.filter(restaurant_id=restaurant_id)
    return render(request, 'restaurant/detail.html',context={'restaurant':restaurant,'serves':serves})

@login_required
def like(request, restaurant_id):
    if (request.method == 'GET'):
        # restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
        # restaurant.likes = restaurant.likes + 1
        # restaurant.save()
        c = connection.cursor()
        c.execute('SELECT likes FROM "restaurant_restaurant" WHERE id = ' + str(restaurant_id))
        count = c.fetchall()
        mydata = c.execute('UPDATE restaurant_restaurant SET likes = '+ str(count[0][0] + 1) +' WHERE id = ' + str(restaurant_id))
        connection.commit()
        return redirect('/restaurant/'+ str(restaurant_id))

@login_required
def delete(request, restaurant_id):
    if (request.method == 'POST'):
        # restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
        # restaurant.delete()
        #return render(request, 'restaurant/home.html')
        #Restaurant.objects.raw('DELETE FROM "restaurant_restaurant" WHERE id = ' + str(restaurant_id))
        
        c = connection.cursor()
        mydata = c.execute('DELETE FROM "serves_serves" WHERE id=' + str(restaurant_id))
        mydata = c.execute('DELETE FROM "restaurant_restaurant" WHERE id=' + str(restaurant_id))
        # conn.commit()
        # c.close
        restaurants = Restaurant.objects.raw('SELECT * FROM "restaurant_restaurant"')
        return render(request,'index.html',{'restaurants':restaurants})


@login_required
def search(request):
    query = request.GET['searchbar']
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
        category_query += " AND bool_or(r.is_veg) = TRUE"
    if isDessert:
        category_query +=  " AND bool_or(is_dessert) = TRUE"
    if isFine:
        category_query +=  " AND bool_or(is_finedining) = TRUE"
    if isNight:
        category_query +=  " AND bool_or(is_nightlife) = TRUE"
    if isCafe:
        category_query +=  " AND bool_or(is_cafe) = TRUE"

    
    c = connection.cursor()
    c.execute(
        "SELECT r.name FROM restaurant_restaurant AS r \
        LEFT JOIN serves_serves AS s ON r.id = s.restaurant_id_id \
        WHERE r.name LIKE %s OR r.cuisine LIKE %s OR r.location LIKE %s OR s.dname LIKE %s\
        GROUP BY r.name HAVING MIN(s.price) >= " + min + " AND MAX(s.price) <= "+ max +" \
        AND SUM(s.likes) >= " + str(likes) + " \
        " + category_query
        , ['%'+request.GET['searchbar']+'%','%'+request.GET['searchbar']+'%','%'+request.GET['searchbar']+'%','%'+request.GET['searchbar']+'%'])
    restaurants = c.fetchall()
    # restaurants.filter()
    print("restaurant", restaurants)
    print("type", type(restaurants))
    # restaurants = Restaurant.objects.raw("SELECT * FROM 'restaurant_restaurant' WHERE name LIKE '%" + request.GET['searchbar'] + "%'")
    # restaurants = Restaurant.objects.raw("SELECT * FROM restaurant_restaurant WHERE name ='" + request.GET['searchbar'] + "'")

    # print(len(restaurants))
    # restaurants = Restaurant.objects.filter(name__icontains=query)
    return render(request,'restaurant/search.html',{'search_results':restaurants})


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
