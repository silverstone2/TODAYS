from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name="main"),
    path('result/', views.result, name="result"),
    path('users/login/', views.login, name="login"),
    path('users/signup/', views.signup, name="signup"),
    path('users/mypage/', views.mypage, name="mypage"),
]
