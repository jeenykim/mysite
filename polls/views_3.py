from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice,Question

# 함수기반뷰를 충분히 연습해야함

# Django의 제네릭 뷰를 사용할 때, 각 뷰가 어떤 모델과 상호 작용할지를 정의해야 한다
# 이를 위해서는 model 속성을 사용하거나 (model = Question와 같이) get_queryset() 메서드를 정의하여 제공해야 한다

# 각 제네릭 뷰는 어떤 모델과 상호 작용할지를 알아야 한다. 
# 이는 model 속성을 사용하여 정의될 수 있다 (예: model = Question은 DetailView 및 ResultsView에서 사용됨) 또는 get_queryset() 메서드를 정의함으로써 제공할 수 있다 (IndexView에서 보여진 것처럼).
    
# Django의 제네릭 뷰는 특정 모델과 연결되어 작동하며, 이 모델은 model 속성을 통해 또는 get_queryset() 메서드를 통해 제공된다. 
# model 속성을 사용하면 모델을 직접 지정할 수 있고, get_queryset() 메서드를 사용하면 필요한 쿼리셋을 동적으로 정의할 수 있다.

# 15 제너릭 뷰 수정:model 속성을 사용하여 코드 간결화
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    # ListView 제네릭 뷰는 <app name>/<model name>_list.html 템플릿을 기본으로 사용한다
    # 이미 있는 "polls/index.html" 템플릿을 사용하기 위해 ListView 에 template_name 를 전달했다.
    
     # 튜토리얼의 이전 부분에서 템플릿은 question 및 latest_question_list 컨텍스트 변수를 포함하는 컨텍스트와 함께 명시되었다. 
     
#################################
# 컨텍스트 변수(Context Variable)는 주로 웹 프레임워크에서 템플릿(Template)과 뷰(View) 간의 데이터 교환을 위해 사용되는 변수이다. 
# 대표적으로 Django, Flask 등의 웹 프레임워크에서 사용되며, 뷰에서 생성한 데이터를 템플릿에 전달하여 동적으로 웹 페이지를 구성하는 데 활용된다.
# Django에서는 뷰 함수에서 render 함수를 통해 템플릿을 렌더링할 때, 추가적인 데이터를 context라는 딕셔너리 형태로 전달한다. 
# 이 context 딕셔너리에 포함된 값들은 템플릿에서 변수로 사용되며, 이러한 변수를 컨텍스트 변수라고 한다.
#################################
    
    # DetailView 의 경우 question 변수가 자동으로 제공되는데, 이는 우리가 Django 모델(Question)을 사용하고 있기 때문에 Django가 컨텍스트 변수의 적절한 이름을 결정할 수 있다. 
    # 그러나 ListView의 경우 자동으로 생성되는 컨텍스트 변수는 question_list이다. 
    # 이것을 덮어 쓰려면 context_object_name 속성을 제공하고, 대신에 latest_question_list 를 사용하도록 지정해야한다. 
    # 새로운 기본 컨텍스트 변수와 일치하도록 템플릿을 변경할 수도 있지만, 원하는 변수를 사용하도록 Django에게 지시하는 것이 훨씬 쉽다.
    
    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]
    
    #마지막에 발행된 다섯 개의 질문을 화면에 반환한다.
    # get_queryset 메서드는 제네릭 뷰에서 특정 쿼리셋을 정의하는 데 사용된다.
    # 이 메서드에서는 Question 모델의 객체들을 pub_date를 기준으로 내림차순으로 정렬하고, 처음 다섯 개의 객체만을 포함하는 쿼리셋을 반환한다.
    # 이렇게 정의된 쿼리셋은 해당 뷰에서 사용되어 클라이언트에게 제공된다.
    
   
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
    # 기본적으로 DetailView 제너릭 뷰는 <app name>/<model name>_detail.html 템플릿을 사용한다. 
    # "polls/question_detail.html"템플릿을 사용할 것이다. template_name 속성은 Django에게 자동 생성 된 기본 템플릿 이름 대신에 특정 템플릿 이름을 사용하도록 알려주기 위해 사용된다.
    # Django의 Question 클래스는 데이터베이스에서 질문을 나타내기 위한 모델(Model) 클래스이다. 
    # Django에서는 모델을 사용하여 데이터베이스 테이블을 정의하고 데이터에 접근하는 방법을 제공한다. 
    # Question 모델은 대부분의 웹 애플리케이션에서 사용되는 데이터를 저장하는 데 예시로 사용되는 일반적인 모델이다. 


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    # results리스트 뷰에 대해서 template_name을 지정한다 


# 이전과 동일함
# 14 간단한 폼쓰기 추가
def vote(request, question_id):
    # 주어진 question_id에 해당하는 Question 객체를 가져옴
    question = get_object_or_404(Question, pk=question_id)
    # get_object_or_404: 주어진 question_id에 해당하는 Question 객체를 데이터베이스에서 가져옴. 
    # 만약 해당 객체가 없으면 404 에러를 발생시킴
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        # POST 요청에서 선택된 choice를 가져옴
        # request.POST 는 키로 전송된 자료에 접근할 수 있도록 해주는 사전과 같은 객체
        # 이 경우, request.POST['choice'] 는 선택된 설문의 ID를 문자열로 반환
        # request.POST 의 값은 항상 문자열들이다.
    except (KeyError, Choice.DoesNotExist):
        # 선택한 선택지가 없거나 에러가 발생하면 에러 메시지를 표시하고 다시 투표 페이지를 렌더링한다
        # 만약 POST 자료에 choice 가 없으면, request.POST['choice'] 는 KeyError 가 일어난다. 
        # KeyError 를 체크하고, choice가 주어지지 않은 경우에는 에러 메시지와 함께 설문조사 폼을 다시보여준다.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "선택하지 않았어요.",
            },
        )
    else:
        # 선택된 choice의 투표 수를 증가시키고 저장
        selected_choice.votes += 1
        selected_choice.save()
       # 투표가 성공적으로 처리되면 해당 질문의 결과 페이지로 이동
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    # 설문지의 수가 증가한 이후에, 코드는 일반 HttpResponse 가 아닌 HttpResponseRedirect 를 반환하고, HttpResponseRedirect 는 하나의 인수를 받는다#
    # 그 인수는 사용자가 재전송될 URL 이다. 
    
    # HttpResponseRedirect 생성자 안에서 reverse() 함수를 사용하고 있다.#
    # 이 함수는 뷰 함수에서 URL을 하드코딩하지 않도록 도와준다.# #제어를 전달하기 원하는 뷰의 이름을, URL패턴의 변수부분을 조합해서 해당 뷰를 가리킨다.##설정했던 URLconf를 사용하였으며, 이 reverse() 호출은 "/polls/3/results/" 문자열을 반환할 것이다.#
    # 여기서 3 은 question.id 값
    # 이렇게 리디렉션된 URL은 최종 페이지를 표시하기 위해 'results' 뷰를 호출한다.
