from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Restaurant
from django.shortcuts import HttpResponseRedirect,Http404,HttpResponse,render_to_response,get_object_or_404,get_list_or_404
from django.db import models, connection
# Create your views here.
# def home(request):
#     return render(request,'restaurant/home.html')
def home(request):
    res_name = 'Cravings'
    result = get_list_or_404(Restaurant)  
    results = Restaurant.objects.raw('SELECT * FROM "restaurant_restaurant"')
    return render(request, 'index.html', {'results': results})

@login_required
def create(request):
    if (request.method == 'POST'):
        if request.POST['rname'] and request.POST['cuisine'] and request.POST['location'] and request.POST['url'] and request.POST['phone']:
            # restaurant = Restaurant()
            # restaurant.name = request.POST['rname']
            # restaurant.cuisine = request.POST['cuisine']
            # restaurant.location = request.POST['location']
            # restaurant.url = request.POST['url']
            # restaurant.phone = request.POST['phone']
            # restaurant.save()
            c = connection.cursor()
            c.execute("INSERT INTO restaurant_restaurant (name, cuisine, location, url, likes, phone) VALUES ( ' " 
                + request.POST['rname'] + " ' , ' "  
                + request.POST['cuisine'] + " ' , ' "
                + request.POST['location'] + " ' , ' "
                + request.POST['url'] + " ' , ' "
                + str(1) + " ' , ' "
                + request.POST['phone']  + " ' ) "
                )
            results = Restaurant.objects.raw('SELECT id FROM "restaurant_restaurant"')
            print(results[:-1])
            connection.commit()
            return redirect('/restaurant/'+ results[:-1])
        else:
            return render(request,'restaurant/create.html',{'error':'All fields required'})
    else:
        return render(request,'restaurant/create.html')


def detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
    return render(request, 'restaurant/detail.html',{'restaurant':restaurant})

@login_required
def like(request, restaurant_id):
    if (request.method == 'POST'):
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
        restaurants = Restaurant.objects
        return render(request,'restaurant/home.html',{'restaurants':restaurants})
