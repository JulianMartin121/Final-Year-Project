from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from functools import wraps

# Create your views here.
def home(request):
    context = {}
    return render(request, 'homepage/home.html', context)

# def role_required(request):
#     # Decorator to check if the user is within the given role
#     def decorator(view_func):
#         @warps(view_func):
#         def wrapper(request, *args, **kwargs):
#             if request.user.user_type in roles:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return HttpResponseForbidden()
#         return wrapper
#     return decorator


@login_required
def module1(request):
    context = {}
    return render(request, 'homepage/module1.html', context)

@login_required
def module2(request):
    context = {}
    return render(request, 'homepage/module2.html', context)

@login_required
def module3(request):
    context = {}
    return render(request, 'homepage/module3.html', context)




