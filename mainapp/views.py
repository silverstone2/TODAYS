from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from mainapp import functions as func  # 기능 함수들 모두 functions.py 로 분리
# 로그인에 필요한 내장 함수 사용
from django.contrib.auth.models import User
from django.contrib import auth

from mainapp.templates.users.forms import UserForm


# 로그인 구현 중

#  기본값: 서울
nx_ny = {'x': "60", 'y': "127"}
sel_lat_long = {'x': "60", 'y': "127"}
current_location = {'dist1': "서울특별시", 'dist2': "중구"}
selected_location = {'dist1': "서울특별시", 'dist2': "중구"}
current_weather = {}
# 온도 TMP / 강수량 PCP / 풍속 WSD / 습도 REH / 적설량 SNO / 전운량1 - 10(범주)
selected_weather = {}


def main(request):
    return render(request, 'main.html')


def result(request):
    if request.method == 'POST':
        background = "/static/videos/rainy.mp4"

        lat = request.POST.get('startLat')
        long = request.POST.get('startLon')
        location = "판교로 242"  # 임시 주소명

        global current_location
        current_location = func.coord_to_loc(lat, long)

        global nx_ny
        nx_ny = func.grid(lat, long)

        global current_weather
        current_weather = func.dangi_api(nx_ny['x'], nx_ny['y']).get('weather')

        global sel_lat_long
        sel_lat_long = func.geocoder(location)
        sel_nx_ny = func.grid(sel_lat_long['x'], sel_lat_long['y'])

        context = {
            'background': background,
            'latitude': nx_ny['x'],
            'longitude': nx_ny['y'],
            'selected_latitude': sel_nx_ny['x'],
            'selected_longitude': sel_nx_ny['y'],
            'current_tmp': current_weather['tmp'],
            'current_location1': current_location['dist1'],
            'current_location2': current_location['dist2'],
        }
        return render(request, 'main.html', context)
    else:
        # 날씨 정보 차단시 default 값 출력.
        background = "/static/videos/rainy.mp4"
        context = {
            'background': background
        }
    return render(request, 'result.html', context)


def login(request):
    return render(request, 'users/login.html')


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})


def mypage(request):
    return render(request, 'users/mypage.html')

