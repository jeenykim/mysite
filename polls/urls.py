from django.urls import path

from . import views

# 장고에서 지원하는 url 패턴의 규칙


# 13.URL의 이름공간 정하기추가
app_name = "polls"

# 15 제너릭 뷰 수정
# urlpatterns = [
#     # ex: /polls/
#     path("", views.index, name="index"),
#     # 주소창에 url패턴이 아닌 name값을 입력하면 됨
   
    
#     # ex: /polls/5/
#     # 수정
#     # path("<int:question_id>/", views.detail, name="detail"),
#     # question_id로 5를 호출하면 5의 상세페이지가 url주소에 출력됨
#       # views.py의 question_id와 같아야함
      
      
#     # 12.URL 제거하기  수정
#     # path("specifics/ <int:question_id>/", views.detail, name="detail"),
    
#     # 13.URL의 이름공간 정하기 수정
#     #  다시 원상 되돌림
#     path("<int:question_id>/", views.detail, name="detail"),
    
    
    
#     # ex: /polls/5/results/
#     path("<int:question_id>/results/", views.results, name="results"),
#      # views.py의 question_id와 같아야함
    
#     # ex: /polls/5/vote/
#     path("<int:question_id>/vote/", views.vote, name="vote"),
# ]


# 15 제너릭 뷰 수정
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]

# Django에서 제네릭 뷰(Generic Views)는 일반적인 웹 개발 패턴을 구현하는 데 도움을 주기 위해 미리 정의된 뷰 클래스를 제공하는 기능이다
# 제네릭 뷰는 재사용 가능하며, 일반적인 작업을 처리하는 데 필요한 코드를 줄일 수 있도록 도와준다. 
# 주로 모델 데이터를 기반으로 하는 CRUD (Create, Read, Update, Delete) 작업을 지원한다.

# 두 번째와 세 번째 패턴의 경로 문자열에서 일치한 패턴의 이름이 <question_id>에서 <pk>로 변경되었다. 
# 이것은 우리가 DetailView 제네릭 뷰를 사용하여 detail() 및 results() 뷰를 대체할 것이기 때문에 필요한 조치이다. 
# DetailView는 URL에서 캡처된 기본 키(primary key) 값을 'pk'라는 이름으로 기대하고 있다."

# 간단히 말해, Django의 DetailView는 URL에서 캡처된 객체의 기본 키를 'pk'라는 이름으로 예상한다. 
# 따라서 URL 패턴에서 이 이름을 사용하는 것이 일반적으로 권장되는 관례이다. 
# 문장에서 언급된 <question_id>는 URL에서 캡처되는 질문 객체의 기본 키를 나타낸다. 
# 이를 <pk>로 변경함으로써 DetailView가 정상적으로 동작하도록 하는 것이다.