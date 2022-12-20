from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name="main"),
    path('result/', views.result, name="result"),
    path('users/loginform/', views.login, name="login"),
    path('users/loginok/', views.loginok, name="loginok"),
    path('users/signup/', views.signup, name="signup"),
    path('users/signupok/', views.signupok, name="signupok"),
    path('users/mypage/', views.mypage, name="mypage"),
]