from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from functools import wraps

# Create your views here.
def home(request):
    context = {}
    return render(request, 'homepage/home.html', context)

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

@login_required
def module1_home(request):
    context = {}
    return render(request, 'homepage/module1_home.html', context)

@login_required
def module2_home(request):
    context = {}
    return render(request, 'homepage/module2_home.html', context)

@login_required
def module3_home(request):
    context = {}
    return render(request, 'homepage/module3_home.html', context)

@login_required
def course_material_1(request):
    context = {}
    return render(request, 'homepage/course_material_1.html', context)

@login_required
def course_material_2(request):
    context = {}
    return render(request, 'homepage/course_material_2.html', context)

@login_required
def course_material_3(request):
    context = {}
    return render(request, 'homepage/course_material_3.html', context)






