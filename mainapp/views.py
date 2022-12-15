from django.shortcuts import render

# Create your views here.
# def MainFunc(request):
#     return render(request, 'index.html')


def mainapp(request):
    # 임시 날씨에 따라 배경화면 바뀔 예정
    background = "static/videos/rainy.mp4"
    context = {
        'background': background
    }
    return render(request, 'mainapp/main.html', context)
