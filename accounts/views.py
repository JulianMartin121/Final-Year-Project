from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm, TeacherRegistrationForm, StudentLoginForm, TeacherLoginForm

# Create your views here.

# Student registration view
def student_register_request(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:student_login')
    else:
        form = StudentRegistrationForm()
    return render(request=request, template_name="accounts/student_register.html", context={"register_form":form})

# Teacher registration view
def teacher_register_request(request):
    if request.method == "POST":
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:teacher_login')
    else:
        form = TeacherRegistrationForm()
    return render(request=request, template_name="accounts/teacher_register.html", context={"register_form":form})

# Student login view
def student_login_request(request):
    if request.method == "POST":
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            return redirect('homepage:student_home')
    else:
        form = StudentLoginForm()
    return render(request=request, template_name="accounts/student_login.html", context={"login_form":form})

# Teacher login view
def teacher_login_request(request):
    if request.method == "POST":
        form = TeacherLoginForm(request, data=request.POST)
        if form.is_valid():
            return redirect('homepage:teacher_home')
    else:
        form = TeacherLoginForm()
    return render(request=request, template_name="accounts/teacher_login.html", context={"login_form":form})

