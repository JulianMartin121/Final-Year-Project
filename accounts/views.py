from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user_type = form.cleaned_data.get('user_type')
            if user_type == '1':
                user.user_type = 1 # Set user to student
            if user_type == '2':
                user.user_type = 2 # Set user to teacher
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'], 
                            user_type=request.POST['user_type'], uni_id=request.POST['uni_ID'])
        if user is not None:
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def profile_view(request):
    return render(request, 'accounts/profile.html')
