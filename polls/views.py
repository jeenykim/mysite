from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. 성공이야")

# Create your views here.
# view내부의 문구가 클라이언트에게 화면으로 전달
