from django.contrib import admin
from django.urls import path,include
from vocab import views




urlpatterns = [
    path('', views.home, name='home'),
    path('result/', views.result, name='result'),
    path('home/', views.home1, name='home1'),
    path('day/<int:myid>/test',views.test,name="test")

    

]