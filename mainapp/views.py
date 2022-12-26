from django.shortcuts import render, redirect
from mainapp import functions as func  # 기능 함수들 모두 functions.py 로 분리
# 로그인에 필요한 내장 함수 사용
from django.contrib.auth.hashers import make_password, check_password
from mainapp.models import Members, Mybookmark
from datetime import datetime
import re
from django.http import HttpResponseRedirect, JsonResponse
import json


# 모델 예측을 위한 데이터 전처리 모듈
import pickle
import pandas as pd
import numpy as np

# 딥러닝 분류 모델
from .apps import models

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


def main(request):
    return render(request, 'main.html')


def result(request):
    if 'Members' not in request.session:
        return render(request, 'users/loginform.html')

    if request.method == 'POST':
        gu = request.POST.get('sido')
        dong = request.POST.get('gugun')
        mood = request.POST.get('mood')
        food = request.POST.get('food')
        print('responded value:', gu, dong, mood, food)
        try:

            # 선택된 날짜 기반
            global sel_lat_long
            sel_lat_long = func.location_to_coord(gu, dong)
            sel_nx_ny = func.grid(sel_lat_long['lat'], sel_lat_long['long'])
            global selected_weather
            selected_weather = func.dangi_api(sel_nx_ny['x'], sel_nx_ny['y']).get('weather')
            background = func.set_background(hour, selected_weather['code'])

            maxim = func.maxim()

            # 모델 예측을 위한 데이터 전처리
            data = {}

            # [ 자치구 칼럼 전처리 ]
            with open('./mainapp/encoders/자치구_encoder.pickle', 'rb') as f:
                administ_encoder = pickle.load(f)
            administ = administ_encoder.transform([gu])[0]
            data['자치구'] = [administ]

            # [ 행정동 칼럼 전처리 ]
            with open('./mainapp/encoders/자치구별_행정동_encoders.pickle', 'rb') as f:
                building_encoders = pickle.load(f)
            building_encoder = building_encoders[administ]
            building = building_encoder.transform([dong])[0]
            data['행정동'] = [building]

            # [ 카테고리 칼럼 전처리 ]
            with open('./mainapp/encoders/카테고리_encoder.pickle', 'rb') as f:
                category_encoder = pickle.load(f)
            category = category_encoder.transform([food])[0]

            with open('./mainapp/encoders/카테고리_정규화.pickle', 'rb') as f:
                category_scaler = pickle.load(f)
            category = category_scaler.transform([[category]]).flatten()[0]
            data['카테고리'] = [category]

            # [ 분위기 칼럼 전처리 ]
            with open('./mainapp/encoders/분위기 넘버링 데이터.pickle', 'rb') as f:
                mood_dict = pickle.load(f)
            mood_number = [k for k, v in mood_dict.items() if v == mood][0]
            data['분위기'] = [mood_number]

            # [ 평균기온(°C) 칼럼 전처리 ]
            with open('./mainapp/encoders/평균기온_정규화.pickle', 'rb') as f:
                meantemp_scaler = pickle.load(f)
            tmp = float(selected_weather['tmp'])
            meantemp = meantemp_scaler.transform([[selected_weather['tmp']]]).flatten()[0]
            data['평균기온(°C)'] = [meantemp]

            # [ 평균 풍속(m/s) 칼럼 전처리 ]
            wsd = float(selected_weather['wsd'])
            data['평균 풍속(m/s)'] = [wsd]

            # [ 평균 상대습도(%) 칼럼 전처리 ]
            reh = float(selected_weather['reh']) / 100.0
            data['평균 상대습도(%)'] = [reh]

            new_x = pd.DataFrame(data)

            # 모델 예측
            with open('./mainapp/encoders/카페명_encoder.pickle', 'rb') as f:
                cafe_encoder = pickle.load(f)

            data_list_df = pd.read_csv('./mainapp/datasets/Django에서 쓸 데이터프레임.csv')
            data_list_df.drop(['Unnamed: 0'], axis=1, inplace=True)

            model = models[0]
            new_y = model.predict(new_x)
            new_y = new_y.tolist()[0]
            result_df = pd.DataFrame(columns=data_list_df.columns)

            for i in range(5):
                idx = new_y.index(np.max(new_y))
                new_y[idx] = 0.0
                cafe_name = cafe_encoder.inverse_transform([idx])[0]
                test_df = data_list_df[data_list_df['카페명'] == cafe_name]
                result_df = pd.concat([result_df, test_df], axis=0)

            result_df.reset_index(inplace=True)
            result_df.drop(['index'], axis=1, inplace=True)
            # print(result_df)

            # 결과 데이터프레임 loop
            loop = []
            for i, data in enumerate(result_df.values):
                test_dict = {
                    'num': i + 1,
                    'name': data[0],
                    'addr': data[1] + ' ' + data[2],
                    'category': data[3],
                    'mood': data[4],
                    'img_addr': data[-1]
                }
                loop.append(test_dict)
            loop_cnt = len(loop)

            context = {
                'background': background,
                'latitude': nx_ny['x'],
                'longitude': nx_ny['y'],

                'gu': gu,
                'dong': dong,
                'mood': mood,
                'food': food,

                'selected_tmp': selected_weather['tmp'],  # 온도 TMP
                'selected_pcp': selected_weather['pcp'],  # 강수량 PCP ( 범주 )
                'selected_wsd': selected_weather['wsd'],  # 풍속 WSD
                'selected_reh': selected_weather['reh'],  # 습도 REH
                'selected_sno': selected_weather['sno'],  # 1시간 신적설 SNO ( 범주 )
                'selected_sky': selected_weather['sky'],  # 전운량 1, 2, 4(범주)
                'selected_latitude': sel_nx_ny['x'],
                'selected_longitude': sel_nx_ny['y'],

                'maxim_author': maxim['author'],
                'maxim_message': maxim['message'],

                'loop': loop,
                'loopCnt': loop_cnt,
            }
            return render(request, 'result.html', context)
        except Exception as e:
            return render(request, 'mainErr.html')
    else:
        # 날씨 정보 차단시 default 값 출력.
        background = ""
        context = {
            'background': background
        }
    return render(request, 'result.html', context)


def bookmark(request):  # checkForm 함수로 작동하는 함수.
    if request.method == 'POST':
        my_id = request.session.get('Members', '')  # 아이디
        cafe_cnt = request.POST.get("cafeCnt")
        cafes = {1: request.POST.get("cafe1value"), 2: request.POST.get("cafe2value"),
                 3: request.POST.get("cafe3value"), 4: request.POST.get("cafe4value"),
                 5: request.POST.get("cafe5value")}
        cafes_addr = {1: request.POST.get("cafe1addr"), 2: request.POST.get("cafe2addr"),
                      3: request.POST.get("cafe3addr"), 4: request.POST.get("cafe4addr"),
                      5: request.POST.get("cafe5addr")}
        cafe_mood = request.POST.get("mood")
        cafe_food = request.POST.get("food")
        print(cafes)
        context = {
            'cafe_cnt': cafe_cnt,
        }
        for num in range(1, 6):
            if cafes[num] == "":
                pass
            else:
                new_my_bookmark = Mybookmark()
                new_my_bookmark.id = my_id
                new_my_bookmark.cafename = cafes[num]
                new_my_bookmark.addr = cafes_addr[num]
                new_my_bookmark.mood = cafe_mood
                new_my_bookmark.category = cafe_food
                new_my_bookmark.save()
        return render(request, 'bookmarkOk.html', context)
    else:
        return render(request, '/')

def login(request):
    lo_err = {}
    if request.method == "POST":
        login_id = request.POST.get('lo_id')
        login_pwd = request.POST.get('lo_pwd')
        if not login_id:
            # lo_error['err'] = "아이디와 비밀번호 모두 입력하세요"
            return render(request, 'users/inserterr.html')
        if login_id:
            try:
                members = Members.objects.get(id=login_id)
            except Exception as e:
                print(e)
                return render(request, 'users/iderr.html')
        if check_password(login_pwd, members.pw1):
            request.session['Members'] = members.id
            request.session['Members1'] = members.name
            request.session['Members2'] = members.email
            request.session['Members3'] = str(members.regdate)
            return redirect('/')
        else:
            return render(request, 'users/pwderr.html')
    return render(request, 'users/loginform.html')


def loginform(request):
    return render(request, 'users/loginform.html')


# 회원가입 페이지로 이동
def signup(request):
    return render(request, 'users/signup.html')


# POST 방식으로 각 항목들을 받아서 Err가 없으면 데이터베이스에 값을 삽입하고 회원가입 완료
def signupok(request):
    try:
        if request.method == "POST":
            name = request.POST.get('members_name')
            id = request.POST.get('members_id')
            pw1 = request.POST.get('members_pw1')
            pw2 = request.POST.get('members_pw2')
            email = request.POST.get('members_email')
            PASSWORD_VALIDATION = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            err_data = {}
            if not(id and name and pw1 and pw2):
                return render(request, 'users/signupInputErr.html')
            elif pw1 != pw2:
                return render(request, 'users/signupPwdErr.html')
            elif not re.match(PASSWORD_VALIDATION, pw1):
                return render(request, 'users/valiErr.html')

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
    except Exception as e:
        return render(request, 'users/signupIdErr.html')


def logout(request):
    request.session.flush()
    return redirect('/')


def mypage(request):
    if 'Members' not in request.session:
        return render(request, 'users/loginform.html')
    context = {}
    context['m_id'] = request.session.get('Members', '')
    context['m_name'] = request.session.get('Members1', '')
    context['m_email'] = request.session.get('Members2', '')
    context['m_regdate'] = request.session.get('Members3', '')

    return render(request, 'users/mypage.html', context)

def err(request):
    return render(request, 'err.html')


def pwderr(request):
    return render(request, 'users/pwderr.html')


def inserterr(request):
    return render(request, 'users/inserterr.html')


def iderr(request):
    return render(request, 'users/iderr.html')

def signupPwdErr(request):
    return render(request, 'users/signupPwdErr.html')

def signupInputErr(request):
    return render(request, 'users/signupInputErr.html')


def signupIdErr(request):
    return render(request, 'users/signupIdErr.html')


def valiErr(request):
    return render(request, 'users/valiErr.html')
    
def mylike(request):
    if 'Members' not in request.session:
        return render(request, 'users/loginform.html')

    myid = request.session.get('Members', '')
    likes = Mybookmark.objects.filter(id=myid)
    return render(request, 'users/mylike.html', {'likes': likes})


def delete(request):
    delRec = Mybookmark.objects.get(bookmarkno=request.GET.get('bookmarkno'))
    delRec.delete()
    return HttpResponseRedirect("/users/mylike")


def modifymemo(request):
    jsonObject = json.loads(request.body)
    memo = Mybookmark.objects.filter(bookmarkno=jsonObject.get('id'))
    context = {
        'result': 'no'
    }
    if memo is not None:
        memo.update(memo=jsonObject.get('content'))
        context = {
            'result': 'ok'
        }
        return JsonResponse(context)
    return JsonResponse(context)
