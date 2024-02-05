from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        print("Form checking now.")
        if form.is_valid():
            user = form.save()
            print(form.cleaned_data)

            raw_username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=raw_username, password=raw_password)

            print(user)

            login(request, user)
            return redirect('home')
        else:
            print("Form worked but not valid.")
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'accounts/login.html', {'form': form})

    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')
