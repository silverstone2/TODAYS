from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.main, name="main"),
    path('result/', views.result, name="result"),
    path('users/loginform/', views.login, name="loginform"),
    path('users/loginok/', views.loginok, name="loginok"),
    path('users/signup/', views.signup, name="signup"),
    path('users/signupok/', views.signupok, name="signupok"),
    path('users/mypage/', views.mypage, name="mypage"),
]