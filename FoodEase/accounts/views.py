from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.

def signup(request):
    if (request.method == 'POST'):
        if (request.POST['password1'] == request.POST['password2']):
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html',{'error':'Username already exists! Try another username.'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html',{'error':'Passwords must match!'})
    else:
        return render(request, 'accounts/signup.html')

def login(request):
    if (request.method == 'POST'):
        name = request.POST['username']
        user = auth.authenticate(username=name,password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            request.session['user_login_name'] = name
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error':'Username or Password is incorrect!' })
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if (request.method == 'POST'):
        auth.logout(request)
        return redirect('home')
    # return render(request, 'accounts/signup.html')
    del request.session['user_login_name']
    return redirect('home')

