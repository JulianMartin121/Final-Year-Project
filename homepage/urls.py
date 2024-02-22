from django.urls import path
from . import views

urlpatterns = [
    path('module1/', views.module1, name='module1'),
    path('module2/', views.module2, name='module2'),
    path('module3/', views.module3, name='module3'),
    path('module1/coursematerials', views.course_material_1, name='course_material_1'),
    path('module2/coursematerials', views.course_material_2, name='course_material_2'),
    path('module3/coursematerials', views.course_material_3, name='course_material_3'),
    path('', views.home, name='home'),
]

