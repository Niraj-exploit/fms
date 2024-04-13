from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import myUserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import User


def registerPage(request):
    form = myUserCreationForm()

    if request.method == 'POST':
        form = myUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f' {error}')

    return render(request, 'userAuth/register.html', {'form': form})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(request.POST)


        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return render(request, 'userAuth/login.html')

        authenticated_user = authenticate(request, username=username, password=password)

        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not match')

    context = {}
    return render(request, 'userAuth/login.html', context)


def landingPage(request):
    return render (request, 'userAuth/landing.html')

def ownerRegisterPage(request):
    form = myUserCreationForm()
    
    if request.method == 'POST':
        form = myUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.is_futsal_owner = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f' {error}')
    context = {
        'form': form
    }
    return render(request, 'userAuth/owner_register.html', context)

