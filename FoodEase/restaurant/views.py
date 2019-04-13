from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Restaurant
from dish import models as dish_models
from serves import models as serves_models

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
            restaurant.save()
            return redirect('/restaurant/'+ str(restaurant.id))
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
    if (request.method == 'POST'):
        restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
        restaurant.likes += 1
        restaurant.save()
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
