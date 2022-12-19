from django.shortcuts import render
from mainapp import functions as func  # 기능 함수들 모두 functions.py 로 분리
import pandas as pd

#  기본값: 서울
nx_ny = {'x': "60", 'y': "127"}
sel_lat_long = {'x': "60", 'y': "127"}
current_location = {'dist1': "서울특별시", 'dist2': "중구"}
selected_location = {'dist1': "서울특별시", 'dist2': "중구"}
current_weather = {}
# 온도 TMP 강수량 PCP 풍속 WSD 습도 REH 적설량 SNO 전운량1 - 10(범주)
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


def checkin(request):
    context = {
    }
    return render(request, 'checkin.html', context)


def login(request):
    return render(request, 'users/login.html')


def signup(request):
    return render(request, 'users/signup.html');

