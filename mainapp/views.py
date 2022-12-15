from django.shortcuts import render
import googlemaps
import requests # HTTP 요청을 보내는 모듈
import datetime # 날짜시간 모듈
import json  # json 파일 파싱하여 데이터 읽는 모듈

gmaps = googlemaps.Client(key="AIzaSyBTmrYMwJez4u2jczuI3Fhpj1SLrMxRDnU")
village_weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
service_key = "1HyN5CpAcCICizuwcx%2FW0DBWu3icqrH%2BUNPl3PiC9HxqEyn7764WVIf9sLA4ei%2FGNKHVCHbSxi%2B63Py7VqwnMg%3D%3D"
today = datetime.datetime.today()
base_date = today.strftime("%Y%m%d")  # "20200214" == 기준 날짜
base_time = "0800"  # 날씨 값
nx = "60"  # 기본 좌표값
ny = "128"  # 기본 좌표값


def main(request):
    if request.method == 'POST':
        background = "/static/videos/rainy.mp4"
        nx = request.POST.get('startLat') #nx
        ny = request.POST.get('startLon') #ny
        payload = "serviceKey=" + service_key + "&" + \
                  "dataType=json" + "&" + \
                  "base_date=" + base_date + "&" + \
                  "base_time=" + base_time + "&" + \
                  "nx=" + nx + "&" + \
                  "ny=" + ny
        weather_result = requests.get(village_weather_url + payload)
        items = weather_result.json().get('response').get('body').get('items')
        print(items)
        context = {
            'background': background,
            'latitude': nx,
            'longitude': ny,
        }
        return render(request, 'mainapp/main.html', context)
    else:
        # 날씨 정보 차단시 default 값 출력.
        background = "/static/videos/rainy.mp4"
        context = {
            'background': background
        }
        return render(request, 'mainapp/main.html', context)


def checkin(request):
    context = {
    }
    return render(request, 'mainapp/checkin.html', context)