from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.main, name="main"),
    path('result/', views.result, name="result"),
    path('bookmark/', views.bookmark, name="bookmark"),
    path('users/loginform/', views.loginform, name="loginform"),
    path('users/login/', views.login, name="login"),
    path('users/signup/', views.signup, name="signup"),
    path('users/signupok/', views.signupok, name="signupok"),
    path('users/mypage/', views.mypage, name="mypage"),
    path('users/mylike/', views.mylike, name="mylike"),
    path('users/logout/', views.logout, name="logout"),
    path('users/pwderr/', views.pwderr),
    path('users/inserterr/', views.inserterr),
    path('users/idterr/', views.iderr),
]

