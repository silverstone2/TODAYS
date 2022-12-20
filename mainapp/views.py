from django.shortcuts import render, redirect
from mainapp import functions as func  # 기능 함수들 모두 functions.py 로 분리
from datetime import date, datetime, timedelta

# 로그인 구현 중

#  기본값: 서울
hour = datetime.now().hour
lat = "37.579871128849334"  # 위도
long = "126.98935225645432"  # 경도

nx_ny = {'x': "60", 'y': "127"}
current_weather = {}
current_location = {'dist1': "서울특별시", 'dist2': "중구"}

sel_lat_long = {'lat': "37.579871128849334", 'long': "126.98935225645432"}
selected_weather = {}
selected_location = {'dist1': "서울특별시", 'dist2': "중구"}
# 온도 TMP / 강수량 PCP / 풍속 WSD / 습도 REH / 적설량 SNO / 전운량1 - 10(범주)


def main(request):
    return render(request, 'main.html')


def result(request):
    if request.method == 'POST':
        gu = request.POST.get('sido')
        dong = request.POST.get('gugun')
        feeling = request.POST.get('feeling')
        food = request.POST.get('food')
        print('잘 왓니?:', gu, dong, feeling, food)

        # 현 위치 기반
        global current_location
        current_location = func.coord_to_loc(lat, long)
        global nx_ny
        nx_ny = func.grid(lat, long)
        global current_weather
        current_weather = func.dangi_api(nx_ny['x'], nx_ny['y']).get('weather')

        # 선택된 날짜 기반
        global sel_lat_long
        sel_lat_long = func.location_to_coord(gu, dong)
        sel_nx_ny = func.grid(sel_lat_long['lat'], sel_lat_long['long'])
        global selected_weather
        selected_weather = func.dangi_api(sel_nx_ny['x'], sel_nx_ny['y']).get('weather')

        print(selected_weather['code'])
        background = func.background(hour, selected_weather['code'])
        print(background)
        context = {
            'background': background,
            'latitude': nx_ny['x'],
            'longitude': nx_ny['y'],

            'current_tmp': current_weather['tmp'],
            'current_location1': current_location['dist1'],
            'current_location2': current_location['dist2'],

            'selected_tmp': selected_weather['tmp'],
            'selected_latitude': sel_nx_ny['x'],
            'selected_longitude': sel_nx_ny['y'],
            'gu': gu,
            'dong': dong,
        }
        return render(request, 'result.html', context)
    else:
        # 날씨 정보 차단시 default 값 출력.
        background = ""
        context = {
            'background': background
        }
    return render(request, 'result.html', context)

