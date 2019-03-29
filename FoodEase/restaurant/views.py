from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Restaurant

# Create your views here.
def home(request):
    return render(request,'restaurant/home.html')

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
            return redirect('home')
        else:
            return render(request,'restaurant/create.html',{'error':'All fields required'})
    else:
        return render(request,'restaurant/create.html')
