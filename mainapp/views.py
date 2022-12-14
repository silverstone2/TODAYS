from django.shortcuts import render


# Create your views here.
# def MainFunc(request):
#     return render(request, 'index.html')


def main(request):
    if request.method == 'POST':
        background = "/static/videos/rainy.mp4"
        lat = request.POST.get('startLat')
        lon = request.POST.get('startLon')
        context = {
            'background': background,
            'latitude': lat,
            'longitude': lon,
        }
        print(lat, lon)# 안 받아와 지네 ㅅㅂ
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