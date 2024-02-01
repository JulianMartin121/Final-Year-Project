from django.urls import path
from . import views

urlpatterns = [
    path('module1/', views.module1, name='module1'),
    path('module2/', views.module2, name='module2'),
    path('module3/', views.module3, name='module3'),
    path('', views.home, name='home'),
]

