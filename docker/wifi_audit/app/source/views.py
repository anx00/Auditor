from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.


@login_required(login_url='login')
def home(request):
    return render(request, "source/home.html")


# User must be created from admin panel
def login_page(request):
    if request.user.is_authenticated:
        return redirect('Home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('Home')
            else:
                messages.info(request, 'Incorrect Username or Password')

        context = {}
        return render(request, 'source/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')
