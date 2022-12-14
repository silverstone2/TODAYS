from django.shortcuts import render

# Create your views here.
def MainFunc(request):
    return render(request, 'index.html')