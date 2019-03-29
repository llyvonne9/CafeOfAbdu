from django.http import HttpResponse

def home(request):
	return HttpResponse("Welcome to FoodEase!")

def index(request):
    return render(request, 'index.html')
