from django.urls import path
from . import views

urlpatterns = [
    path('student_register/', views.student_register_request, name="student_register"),
    path('teacher_register/', views.teacher_register_request, name="teacher_register"),
    path('student_login/', views.student_login_request, name="student_login"),
    path('teacher_login/', views.teacher_login_request, name="teacher_login"),
]