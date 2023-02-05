from django.contrib import admin
from django.urls import path,include
from vocab import views




urlpatterns = [
    path('', views.home, name='home'),
    path('result/', views.result, name='result'),
    path('attempt_history/', views.attempt_history, name='attempt_history'),
    path('day/<int:myid>/test',views.test,name="test"),
    path('refresh/',views.refresh,name="refresh"),
    path('signup/', views.handleSignup, name='signup'),
    path('login/', views.handleLogin, name='login'),
    path('logout/', views.handleLogout, name='logout'),

    

]


