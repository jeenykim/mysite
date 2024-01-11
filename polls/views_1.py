from django.http import HttpResponse
from django.http import Http404
# from django.template import loader
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render

from .models import Question

# Create your views here.
# view내부의 문구가 클라이언트에게 화면으로 전달

#1
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     output = ", ".join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)
# question_list중에서 출판일자를 정렬하여 5개까지만 가져오고 ,로 연결하고 문자열화 하여 응답하겠다
# 새로운 index() 뷰 하나를 호출했을 때, 시스템에 저장된 최소한 5 개의 투표 질문이 콤마로 분리되어, 발행일에 따라 출력됩니다.


# 2.template연동
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     template = loader.get_template("polls/index.html")
#     # polls/index.html 템플릿을 불러온 후
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     # context를 전달
#     # 리스트 내용을 담고 template의 index.html의 디자인으로 보여짐
#     # context는 템플릿에서 쓰이는 변수명과 Python 객체를 연결하는 사전형 값이다
#     return HttpResponse(template.render(context, request))


# 8_1.render(shortcuts)
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # render() 함수는 request 객체를 첫번째 인수로 받고, 템플릿 이름을 두번째 인수로 받으며
    
    context = {"latest_question_list": latest_question_list}
    # context 사전형 객체를 세번째 선택적(optional) 인수로 받는다.
 
 #################################   
# 사전형 객체(Dictionary)은 파이썬에서 사용되는 데이터 구조 중 하나로, 키(key)와 값(value)의 쌍으로 이루어진 연관 배열이다. 
# 다른 프로그래밍 언어에서는 해시 맵(Hash Map), 연관 배열(Associative Array), 맵(Map) 등으로 불리기도 한다.
# 사전은 중괄호 {}를 사용하여 생성하며, 각 키와 값은 콜론(:)으로 연결된다. 
# 여러 개의 키-값 쌍은 콤마(,)로 구분된다. 
# 키는 일반적으로 문자열이나 숫자 등 다양한 데이터 타입을 사용할 수 있다. 
# 템플릿에서 변수나 제어 구조와 같은 동적인 내용을 생성하는 데 사용된다.
 #################################
    
    # context는 템플릿(Template)에 전달되는 데이터를 담은 사전형 객체를 나타낸다. 
    # 템플릿은 이 context를 사용하여 동적으로 데이터를 렌더링하고 화면에 표시한다.
    # 인수로 지정된 context로 
    
    return render(request, "polls/index.html", context)
#  표현된 템플릿의 HttpResponse 객체가 반환된다.

# 모든 뷰에 적용한다면, 더 이상 loader와 HttpResponse를 가져오지 않아도 된다. 
# (만약 detail, results, vote에서 stub 메소드를 가지고 있다면, HttpResponse를 유지해야 한다.)



# 1
# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# 9_1.404에러 추가
def detail(request, question_id):
    # Django의 뷰(View) 함수 중 하나인 detail 함수를 정의
    # 특정 질문의 상세 정보를 보여주는 데 사용
    # Django의 기본적인 예외 처리 및 데이터베이스 조회를 통한 데이터 가져오기를 보여주다.
    # # request: HTTP 요청 객체로, 뷰 함수가 클라이언트의 요청을 처리하는 데 사용된다.
# question_id: URL에서 전달되는 매개변수로, 특정 질문을 식별하는 데 사용된다.
    try:
        # 주어진 question_id에 해당하는 Question 객체를 데이터베이스에서 가져옴
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("질문이 존재하지 않습니다")
    # 만약 해당 question_id에 해당하는 객체가 없으면 Http404 예외를 발생시킴
    return render(request, "polls/detail.html", {"question": question})
 # 가져온 Question 객체를 사용하여 템플릿("polls/detail.html")에 전달하여 HTML을 생성하고, 그 결과를 클라이언트에 반환
# 뷰는 요청된 질문의 ID 가 없을 경우 Http404 예외를 발생시킨다

# 10_1 단축기능

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    #데이터베이스에서 객체를 가져오고, 만약 해당 객체가 존재하지 않을 경우 404 예외를 발생시키는 유틸리티 함수이다
    # 이를 통해 코드가 더 간결해지고 가독성이 향상된다.
    # # Question 모델에서 pk (Primary Key)가 question_id와 일치하는 객체를 데이터베이스에서 가져온다.
    # 만약 해당 객체가 존재하지 않으면, Http404 예외가 자동으로 발생하고 클라이언트에게 404 페이지가 반환된다.
    
    return render(request, "polls/detail.html", {"question": question})
# 가져온 Question 객체는 템플릿에 전달되어 HTML을 생성하고 클라이언트에게 반환된다.

# get_object_or_404() 함수는 Django 모델을 첫번째 인자로 받고, 몇개의 키워드 인수를 모델 관리자의 get() 함수에 넘긴다. 만약 객체가 존재하지 않을 경우, Http404 예외가 발생한다.


#  get_object_or_404() 함수처럼 동작하는 get_list_or_404() 함수가 있다. 
#  get() 대신 filter() 를 쓴다는 것이 다르다. 
#  리스트가 비어있을 경우, Http404 예외를 발생시킨다.


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
