from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Restaurant
from dish import models as dish_models
from serves import models as serves_models
from likes import models as likes_models
from visits import models as visits_models
from django.db.models import Max

# Create your views here.
def home(request):
    restaurants = Restaurant.objects
    return render(request,'restaurant/home.html',{'restaurants':restaurants})

@login_required
def create(request):
    if (request.method == 'POST'):
        if request.POST['rname'] and request.POST['cuisine'] and request.POST['location'] and request.POST['url'] and request.POST['phone']:
            restaurant = Restaurant()
            restaurant.name = request.POST['rname']
            restaurant.cuisine = request.POST['cuisine']
            restaurant.location = request.POST['location']
            restaurant.url = request.POST['url']
            restaurant.phone = request.POST['phone']
            if 'veg' in request.POST:
                restaurant.is_veg = True
            if 'dessert' in request.POST:
                restaurant.is_dessert = True
            if 'night' in request.POST:
                restaurant.is_nightlife = True
            if 'cafe' in request.POST:
                restaurant.is_cafe = True
            if 'fine' in request.POST:
                restaurant.is_finedining = True
            restaurant.save()
            return redirect('/restaurant/'+ str(restaurant.id))
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
        restaurant.num_likes += 1
        restaurant.save()
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
        return redirect('/restaurant/'+ str(restaurant.id))


@login_required
def delete(request, restaurant_id):
    if (request.method == 'POST'):
        restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
        restaurant.delete()
        #return render(request, 'restaurant/home.html')
        restaurants = Restaurant.objects
        return render(request,'restaurant/home.html',{'restaurants':restaurants})

def search(request):
    query = request.GET['searchbar']
    restaurants = Restaurant.objects.filter(name__icontains=query)
    return render(request,'restaurant/search.html',{'restaurants':restaurants})

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
            return render(request,'restaurant/home.html',{'restaurants':restaurants})

@login_required
def like_dish(request, restaurant_id, serve_id):
    restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
    serve = get_object_or_404(serves_models.Serves, pk = serve_id)
    serve.likes += 1
    serve.save()
    return redirect('/restaurant/'+ str(restaurant.id))

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
    del(recommend_dict[key_1])
    key_2 = max(recommend_dict, key=recommend_dict.get)

 

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

    return render(request,'restaurant/recommend.html',{'restaurants':restaurants})
