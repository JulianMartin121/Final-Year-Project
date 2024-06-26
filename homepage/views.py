from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from functools import wraps
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Message, CustomUser


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
    user_type = request.user.user_type
    uni_id = request.user.Uni_ID
    context = {'user_type': user_type, 'Uni_ID': uni_id} 
    if user_type == 'teacher':
        students = CustomUser.objects.filter(user_type='student')
        context['students'] = students
    return render(request, 'homepage/course_material_1.html', context)

@login_required
def course_material_2(request):
    user_type = request.user.user_type
    uni_id = request.user.Uni_ID
    context = {'user_type': user_type, 'Uni_ID': uni_id} 
    if user_type == 'teacher':
        students = CustomUser.objects.filter(user_type='student')
        context['students'] = students
    return render(request, 'homepage/course_material_2.html', context)

@login_required
def course_material_3(request):
    user_type = request.user.user_type
    uni_id = request.user.Uni_ID
    context = {'user_type': user_type, 'Uni_ID': uni_id} 
    if user_type == 'teacher':
        students = CustomUser.objects.filter(user_type='student')
        context['students'] = students
    return render(request, 'homepage/course_material_3.html', context)

@csrf_exempt
@require_POST
def new_message(request):
    print('Received data:', request.POST)
    sender_id = request.POST.get('sender')
    receiver_id = request.POST.get('receiver')
    content = request.POST.get('content')

    sender = CustomUser.objects.get(Uni_ID=sender_id)
    receiver = CustomUser.objects.get(Uni_ID=receiver_id)

    message = Message(sender=sender, receiver=receiver, content=content)
    message.save()

    return JsonResponse({'message': 'Message sent successfully'})