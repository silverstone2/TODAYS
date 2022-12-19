from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
import urllib
import googlemaps
import requests
import math
import json  # json 파일 파싱하여 데이터 읽는 모듈
from datetime import date, datetime, timedelta  # 현재 날짜 외의 날짜 구하기 위한 모듈
from django.shortcuts import render

#  기본값은 서울
nx = "60"
ny = "127"
nx1 = "1"
ny1 = "2"


def main(request):
    if request.method == 'POST':
        background = "/static/videos/rainy.mp4"
        global nx, ny
        nx = request.POST.get('startLat')  # nx    위도
        ny = request.POST.get('startLon')  # ny    경도
        grid(nx, ny)
        print("after gird func:", grid_nx1, grid_ny1)
        api(grid_nx1, grid_ny1)

        context = {
            'background': background,
            'latitude': nx,
            'longitude': ny,
        }
        return render(request, 'main.html', context)
    else:
        # 날씨 정보 차단시 default 값 출력.
        background = "/static/videos/rainy.mp4"
        context = {
            'background': background
        }
        return render(request, 'main.html', context)


def checkin(request):
    context = {
    }
    return render(request, 'checkin.html', context)

def login(request):
    return render(request, 'users/login.html')

def signup(request):
    return render(request, 'users/signup.html');

# 위도 경도 기상청 xy 좌표로 변환
def grid(v1, v2):
    print("nx1, ny1 in grid func:", v1, v2)
    RE = 6371.00877 # 지구 반경(km)
    GRID = 5.0      # 격자 간격(km)
    SLAT1 = 30.0    # 투영 위도1(degree)
    SLAT2 = 60.0    # 투영 위도2(degree)
    OLON = 126.0    # 기준점 경도(degree)
    OLAT = 38.0     # 기준점 위도(degree)
    XO = 43         # 기준점 X좌표(GRID)
    YO = 136        # 기1준점 Y좌표(GRID)

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
    ra = math.tan(math.pi * 0.25 + float(v1) * DEGRAD * 0.5)
    ra = re * sf / math.pow(ra, sn)

    theta = float(v2) * DEGRAD - olon
    if theta > math.pi :
        theta -= 2.0 * math.pi
    if theta < -math.pi :
        theta += 2.0 * math.pi
    theta *= sn
    rs['x'] = math.floor(ra * math.sin(theta) + XO + 0.5)
    rs['y'] = math.floor(ro - ra * math.cos(theta) + YO + 0.5)
    nx1 = rs['x']
    ny1 = rs['y']

    global grid_nx1
    grid_nx1 = nx1
    global grid_ny1
    grid_ny1 = ny1
    print('before return grid:', grid_nx1, grid_ny1)
    return grid_nx1, grid_ny1


def api(v1, v2):
    gmaps = googlemaps.Client(key="AIzaSyBTmrYMwJez4u2jczuI3Fhpj1SLrMxRDnU")
    service_key = "1HyN5CpAcCICizuwcx%2FW0DBWu3icqrH%2BUNPl3PiC9HxqEyn7764WVIf9sLA4ei%2FGNKHVCHbSxi%2B63Py7VqwnMg%3D%3D"
    serviceKeyDecoded = unquote(service_key, 'UTF-8')
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    now = datetime.now()
    print("지금은", now.year, "년", now.month, "월", now.day, "일", now.hour, "시", now.minute, "분", now.second, "초입니다.")
    today = datetime.today()  # 현재 지역 날짜 반환
    today_date = today.strftime("%Y%m%d")  # 오늘의 날짜 (연도/월/일 반환)
    print('오늘의 날짜는', today_date)
    yesterday = date.today() - timedelta(days=1)
    yesterday_date = yesterday.strftime('%Y%m%d')
    print('어제의 날짜는', yesterday_date)
    print(v1, v2)
    if now.hour < 2 or (now.hour == 2 and now.minute <= 10):  # 0시~2시 10분 사이
        base_date = yesterday_date  # 구하고자 하는 날짜가 어제의 날짜
        base_time = "2300"
    elif now.hour < 5 or (now.hour == 5 and now.minute <= 10):  # 2시 11분~5시 10분 사이
        base_date = today_date
        base_time = "0200"
    elif now.hour < 8 or (now.hour == 8 and now.minute <= 10):  # 5시 11분~8시 10분 사이
        base_date = today_date
        base_time = "0500"
    elif now.hour <= 11 or now.minute <= 10:  # 8시 11분~11시 10분 사이
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
    print('queryParams 들어가기 전 v1, v2:', v1, v2)

    queryParams = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('base_date'): base_date,
                                   quote_plus('base_time'): base_time, quote_plus('nx'): v1, quote_plus('ny'): v2,
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows'): '60'})
    res = requests.get(url + queryParams,  verify=False)
    items = res.json().get('response').get('body').get('items')
    #print(items)

    weather_data = dict()
    for item in items['item']:
        # 1시간 기온
        if item['category'] == 'TMP':   # 나옴
            weather_data['tmp'] = item['fcstValue']
        # 습도
        if item['category'] == 'REH':   # 나옴
            weather_data['hum'] = item['fcstValue']
        # 하늘상태: 맑음(1) 구름많은(3) 흐림(4)
        if item['category'] == 'SKY':   # 나옴
            weather_data['sky'] = item['fcstValue']
        # 강수 확률
        if item['category'] == 'POP':   # 나옴
            weather_data['pop'] = item['fcstValue']
        # 풍속
        if item['category'] == 'WSD':   # 나옴
            weather_data['wsd'] = item['fcstValue']
        # # 최고 기온
        # if item['category'] == 'TMX':
        #     weather_data['tmx'] = item['fcstValue']
        # # 최저 기온
        # if item['category'] == 'TMN':
        #     weather_data['tmn'] = item['fcstValue']

        # 기상상태
        if item['category'] == 'SKY':
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
    weather_data['weather'] = weather_data

    print()
    # for i in data:
    #    print(data[i])
    # ex) {'code': '0', 'state': '없음', 'tmp': '17'} # 17도 / 기상 이상 없음

    state = weather_data['weather']['state']

    print(today_date[0:4], '년', today_date[4:6], '월', today_date[6:8], '일', base_time, '시의 날씨 데이터입니다.')
    print("기온은", weather_data['weather']['tmp'], "도 입니다.")

    if state == '비':
        print('비가 와요. 우산을 꼭 챙겨주세요!')
    elif state == '비/눈':
        print('비 또는 눈이 와요. 쌀쌀하니 따뜻하게 입어요! 우산도 꼭 챙겨주세요!')
    elif state == '눈':
        print('눈이 와요. 장갑을 꼭 챙기세요!')
    elif state == '소나기':
        print('소나기가 와요. 비가 언제 올지 모르니, 우산을 꼭 챙겨주세요!')
    else:
        print('날씨가 좋네요 :)')
    print("response: ", weather_data)
    '''
    평균기온(°C)TMP   일강수량(mm)PCP   평균 풍속(m/s)WSD   평균 상대습도(%)REH   합계 일사량(MJ/m2)?   일 최심적설(cm)SNO   평균 전운량(1/10)?
    '''
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