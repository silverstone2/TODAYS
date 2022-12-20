from urllib.parse import urlencode, quote_plus, unquote

import requests
import math
from datetime import date, datetime, timedelta
import json


def grid(v1, v2):  # v1 = lat, v2 = ln
    v1 = float(v1)
    v2 = float(v2)
    RE = 6371.00877  # 지구 반경(km)
    GRID = 5.0  # 격자 간격(km)
    SLAT1 = 30.0  # 투영 위도1(degree)
    SLAT2 = 60.0  # 투영 위도2(degree)
    OLON = 126.0  # 기준점 경도(degree)
    OLAT = 38.0  # 기준점 위도(degree)
    XO = 43  # 기준점 X좌표(GRID)
    YO = 136  # 기1준점 Y좌표(GRID)

    DEGRAD = math.pi / 180.0
    RADDEG = 180.0 / math.pi

    re = RE / GRID;
    slat1 = SLAT1 * DEGRAD
    slat2 = SLAT2 * DEGRAD
    olon = OLON * DEGRAD
    olat = OLAT * DEGRAD

    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(math.pi * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn);
    rs = {};

    ra = math.tan(math.pi * 0.25 + (v1) * DEGRAD * 0.5)
    ra = re * sf / math.pow(ra, sn)

    theta = v2 * DEGRAD - olon
    if theta > math.pi:
        theta -= 2.0 * math.pi
    if theta < -math.pi:
        theta += 2.0 * math.pi
    theta *= sn
    rs['x'] = math.floor(ra * math.sin(theta) + XO + 0.5)
    rs['y'] = math.floor(ro - ra * math.cos(theta) + YO + 0.5)
    return rs


def dangi_api(v1, v2):
    # gmaps = googlemaps.Client(key="AIzaSyBTmrYMwJez4u2jczuI3Fhpj1SLrMxRDnU")
    service_key = "1HyN5CpAcCICizuwcx%2FW0DBWu3icqrH%2BUNPl3PiC9HxqEyn7764WVIf9sLA4ei%2FGNKHVCHbSxi%2B63Py7VqwnMg%3D%3D"
    serviceKeyDecoded = unquote(service_key, 'UTF-8')
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    now = datetime.now()
    print("지금은", now.year, "년", now.month, "월", now.day, "일", now.hour, "시", now.minute, "분", now.second, "초입니다.")
    today = datetime.today()  # 현재 지역 날짜 반환
    today_date = today.strftime("%Y%m%d")  # 오늘의 날짜 (연도/월/일 반환)
    yesterday = date.today() - timedelta(days=1)
    yesterday_date = yesterday.strftime('%Y%m%d')
    if now.hour < 2 or (now.hour == 2 and now.minute <= 10):  # 0시~2시 10분 사이
        base_date = yesterday_date  # 구하려는 하는 날짜가 어제의 날짜일 때
        base_time = "2300"
    elif now.hour < 5 or (now.hour == 5 and now.minute <= 10):  # 2시 11분~5시 10분 사이
        base_date = today_date
        base_time = "0200"
    elif now.hour < 8 or (now.hour == 8 and now.minute <= 10):  # 5시 11분~8시 10분 사이
        base_date = today_date
        base_time = "0500"
    elif now.hour < 11 or now.minute <= 10:  # 8시 11분~11시 10분 사이
        base_date = today_date
        base_time = "0800"
    elif now.hour < 14 or (now.hour == 14 and now.minute <= 10):  # 11시 11분~14시 10분 사이
        base_date = today_date
        base_time = "1100"
    elif now.hour < 17 or (now.hour == 17 and now.minute <= 10):  # 14시 11분~17시 10분 사이
        base_date = today_date
        base_time = "1400"
    elif now.hour < 20 or (now.hour == 20 and now.minute <= 10):  # 17시 11분~20시 10분 사이
        base_date = today_date
        base_time = "1700"
    elif now.hour < 23 or (now.hour == 23 and now.minute <= 10):  # 20시 11분~23시 10분 사이
        base_date = today_date
        base_time = "2000"
    else:  # 23시 11분~23시 59분
        base_date = today_date
        base_time = "2300"
    queryParams = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('base_date'): base_date,
                                   quote_plus('base_time'): base_time, quote_plus('nx'): v1, quote_plus('ny'): v2,
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows'): '60'})
    res = requests.get(url + queryParams,  verify=False)
    items = res.json().get('response').get('body').get('items')
    weather_data = dict()
    data = dict()
    for item in items['item']:
        # 기온
        if item['category'] == 'TMP':
            weather_data['tmp'] = item['fcstValue']
        # 강수량(이거 범주로 나오네 시팔)
        if item['category'] == 'PCP':
            weather_data['pcp'] = item['fcstValue']
        # 풍속
        if item['category'] == 'WSD':
            weather_data['wsd'] = item['fcstValue']
        # 습도(상대습도)
        if item['category'] == 'REH':
            weather_data['reh'] = item['fcstValue']
        # 적설량
        if item['category'] == 'SNO':
            weather_data['sno'] = item['fcstValue']
        # 전운량
        if item['category'] == 'SKY':
            weather_data['sky'] = item['fcstValue']
        # 기상상태
        if item['category'] == 'PTY':
            weather_code = item['fcstValue']
            if weather_code == '1':
                weather_state = '비'
            elif weather_code == '2':
                weather_state = '비/눈'
            elif weather_code == '3':
                weather_state = '눈'
            elif weather_code == '4':
                weather_state = '소나기'
            else:
                weather_state = '없음'
            weather_data['code'] = weather_code
            weather_data['state'] = weather_state

    data['weather'] = weather_data
    return data


def geocoder(string):
    api_url = "http://api.vworld.kr/req/address?"
    params = {
        "service": "address",
        "request": "getcoord",
        "crs": "epsg:4326",
        "address": string,  # 주소 넣기
        "format": "json",
        "type": "road",
        "key": "DA702333-E74C-3FA1-BD96-B1D8F8512921"
    }
    response = requests.get(api_url, params=params)
    result = {}
    if response.status_code == 200:
        items = response.json().get('response').get('result').get('point')
        result = {'x': items['y'], 'y': items['x']}  # api에서 x랑 y 좌표값이 다르게 되어있어서...일단 반대로 추출...
    return result


def coord_to_loc(lat, long):
    long = float(long)
    lat = float(lat)
    long = round(long, 4)
    lat = round(lat, 4)
    long = str(long)
    lat = str(lat)
    api_url = "http://api.vworld.kr/req/address?"
    params = {
        "service": "address",
        "request": "getaddress",
        "crs": "epsg:4326",
        "point": "126.9977,37.5682",
        "format": "json",
        "type": "road",
        "key": "DA702333-E74C-3FA1-BD96-B1D8F8512921"
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        items = response.json().get('response').get('result')
        result = {'dist1': items[0]['structure']['level1'],
                  'dist2': items[0]['structure']['level2']}
        return result

'''
POP    강수확률    %    8
PTY    강수형태    코드값    4
PCP    1시간 강수량    범주 (1 mm)    8   o
REH    습도    %    8                   
SNO    1시간 신적설    범주(1 cm)    8   o
SKY    하늘상태    코드값    4
TMP    1시간 기온    ℃    10
TMN    일 최저기온    ℃    10
TMX    일 최고기온    ℃    10
UUU    풍속(동서성분)    m/s    12
VVV    풍속(남북성분)    m/s    12
WAV    파고    M    8
VEC    풍향    deg    10
WSD    풍속    m/s    10
'''


def location_to_coord(gu, dong):
    a_json = open('C:\TODAYS\mainapp\static\json\dong_coords.json', encoding='utf-8')
    coords = json.load(a_json)
    return_coord = {}
    for i in coords:
        if i["gu"] == gu and i["dong"] == dong:
            return_coord = {'lat': i["lat"], 'long': i["lng"]}
    return return_coord


def set_background(hour, code):
    if 7 < hour < 19:  # 주간
        if code == '1':
            back = "/static/videos/rainy.mp4"
        elif code == '2':
            back = "/static/videos/rainy.mp4"
        elif code == '3':
            back = "/static/videos/snow.mp4"
        elif code == '4':
            back = "/static/videos/rainy.mp4"
        else:
            back = "/static/videos/sunny.mp4"
    if hour >= 19 or hour <= 7:  # 야간
        if code == '1':
            back = "/static/videos/rainy-night.mp4"
        elif code == '2':
            back = "/static/videos/rainy-night.mp4"
        elif code == '3':
            back = "/static/videos/snow-night.mp4"
        elif code == '4':
            back = "/static/videos/rainy-night.mp4"
        else:
            back = "/static/videos/sunny-night.mp4"
    return back
