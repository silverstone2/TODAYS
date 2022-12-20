from django.shortcuts import render, redirect
from mainapp import functions as func  # 기능 함수들 모두 functions.py 로 분리
# 로그인에 필요한 내장 함수 사용
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from sqlalchemy.sql.functions import user
from mainapp.models import Members
from datetime import datetime

#  기본값: 서울
nx_ny = {'x': "60", 'y': "127"}
sel_lat_long = {'x': "60", 'y': "127"}
current_location = {'dist1': "서울특별시", 'dist2': "중구"}
current_weather = {}


def main(request):
    if request.method == 'POST':
        background = "/static/videos/rainy.mp4"

        lat = request.POST.get('startLat')
        long = request.POST.get('startLon')
        location = "판교로 242"  # 임시 주소명

        global current_location
        current_location = func.coord_to_loc(lat, long)

        global nx_ny
        print('lat, long of webbrowser:', lat, long)
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
        return render(request, 'main.html', context)

def result(request):
    return render(request, 'result.html')

def login(request):
    return render(request, 'users/login.html')

def loginok(request):
    return render(request, '/')

# 회원가입 페이지로 이동
def signup(request):
    return render(request, 'signup.html')

# POST 방식으로 각 항목들을 받아서 Err가 없으면 데이터베이스에 값을 삽입하고 회원가입 완료
def signupok(request):
    if request.method == "POST":
        name = request.POST.get('members_name')
        id = request.POST.get('members_id')
        pw1 = request.POST.get('members_pw1')
        pw2 = request.POST.get('members_pw2')
        email = request.POST.get('members_email')
        
        err_data = {}
        if not(id and name and pw1 and pw2):
            err_data['error'] = "모든 값을 입력해야 합니다."
        elif pw1 != pw2:
            err_data['error'] = "비밀번호가 틀립니다."
        else:
            Members(
                name=name,
                id=id,
                pw1=make_password(pw1),
                pw2=make_password(pw2),
                email=email
                ).save()
            return redirect('/')
    return render(request, 'main.html')

def logout(request):
    request.session.flush()
    return redirect('/')

def err(request):
    return render(request, 'err.html')

def mypage(request):
    return render(request, 'users/mypage.html')



