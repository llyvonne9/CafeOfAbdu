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
            # restaurant = Restaurant()
            # restaurant.name = request.POST['rname']
            # restaurant.cuisine = request.POST['cuisine']
            # restaurant.location = request.POST['location']
            # restaurant.url = request.POST['url']
            # restaurant.phone = request.POST['phone']
            # restaurant.save()
            c = connection.cursor()
            c.execute("INSERT INTO restaurant_restaurant (name, cuisine, url, location, likes, lat, lng, phone) VALUES ( ' " 
                + request.POST['rname'] + " ' , ' "  
                + request.POST['cuisine'] + " ' , ' "
                + request.POST['url'] + " ' , ' "
                + ' ' + " ' , ' "
                + str(1) + " ' , ' "
                + str(request.POST['lat']) + " ' , ' "
                + str(request.POST['lng']) + " ' , ' "
                + request.POST['phone']  + " ' ) "
                )
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

def search(request):
    # query = request.GET['searchbar']
    # restaurants = Restaurant.objects.filter(name__icontains=query)
    c = connection.cursor()
    # c.execute("SELECT * FROM restaurant_restaurant WHERE name LIKE '%" + request.GET['searchbar'] + "%'")
    c.execute("SELECT * FROM restaurant_restaurant WHERE name LIKE %s OR cuisine LIKE %s OR location LIKE %s", ['%'+request.GET['searchbar']+'%','%'+request.GET['searchbar']+'%','%'+request.GET['searchbar']+'%'])
    restaurants = c.fetchall()
    print(type(restaurants))
    # restaurants = Restaurant.objects.raw("SELECT * FROM 'restaurant_restaurant' WHERE name LIKE '%" + request.GET['searchbar'] + "%'")
    # restaurants = Restaurant.objects.raw("SELECT * FROM restaurant_restaurant WHERE name ='" + request.GET['searchbar'] + "'")

    # print(len(restaurants))
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
            return render(request,'restaurant/home.html',{'restaurants':restaurants})


@login_required
def like_dish(request, restaurant_id, serve_id):
    restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
    serve = get_object_or_404(serves_models.Serves, pk = serve_id)
    serve.likes += 1
    serve.save()
    return redirect('/restaurant/'+ str(restaurant.id))
