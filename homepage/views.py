from django.shortcuts import render

# Create your views here.
def home(request):
    context = {}
    return render(request, 'homepage/home.html', context)

def module1(request):
    context = {}
    return render(request, 'homepage/module1.html', context)

def module2(request):
    context = {}
    return render(request, 'homepage/module2.html', context)

def module3(request):
    context = {}
    return render(request, 'homepage/module3.html', context)




