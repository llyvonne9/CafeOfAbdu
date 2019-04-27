from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

def home(request):
	# return HttpResponse("Welcome to FoodEase!")
	context = {}
	context['data'] = 'Hello World!'
	return render(request,'index.html', context)

def index(request):
	# template = loader.get_template('index.html')
	
# 	context['data'] = 'Hello World!'
# 	return render(request,'index.html', context)
    return render(request, 'index.html', {'data': 2})
