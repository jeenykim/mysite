# 27. 관리자 폼 커스터마이징
# 수십 개의 필드가 있는 관리 폼의 경우에는 직관적인 순서를 선택하는 것이 사용 편리성의 중요한 부분이다.

# from django.contrib import admin

# from .models import Question

# class QuestionAdmin(admin.ModelAdmin):
#  어드민 클래스를 만든 다음
#     fieldsets = [
#         (None, {"fields": ["question_text"]}),
# 클래스내에 우리가 필요로 하는 값을 부여하고 커스터마이징함
#         ("Date information", {"fields": ["pub_date"]}),
#     ]
    
# # fieldsets의 각 튜플의 첫 번째 요소는 fieldset의 제목이다.
    
# admin.site.register(Question, QuestionAdmin)
#admin.site.register()에 두 번째 인수로 전달한다
# 특별한 변경 사항은 “발행일”이 “설문” 필드 앞에 오게 만든다.

# Question 모델을 admin.site.register(Question)에 등록함으로써, 
# Django는 디폴트 폼 표현을 구성 할 수 있었다. 
# 관리 폼이 보이고 작동하는 방법을 커스터마이징하려는 경우가 있다. 
# 객체를 등록 할 때 Django에 원하는 옵션을 알려주면 커스터마이징 할 수 있다.


# 28.관련된 객체 추가
# Question 객체를 생성할 때 여러 개의 Choices를 직접 추가할 수 있게 한다
# 관련된 선택 사항을 위한 슬롯이 세 개 있으며– extra로 지정됨 – 이미 생성된 객체의 “Change” 페이지의 경우에도 빈 세 개의 슬롯이 생긴다.


from django.contrib import admin

from .models import Choice,Question

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    
# Django에게 “Choice 객체는 Question 관리자 페이지에서 편집된다. 기본으로 3가지 선택 항목을 제공함.” 이라고 알려준다.
# 관련된 선택 사항을 위한 슬롯이 세 개 있으며– extra로 지정됨 – 이미 생성된 객체의 “Change” 페이지의 경우에도 빈 세 개의 슬롯이 생긴다.


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    
    # 29 관리자 변경 목록(change list) 커스터마이징  추가
    # Django는 각 객체의 str()을 표시
    # 개별 필드를 표시 할 수 있으려면 list_display admin 옵션을 사용한다. 
    # 이 옵션은 객체의 변경 목록 페이지에서 열로 표시 할 필드 이름들의 튜플이다.
    list_display = ["question_text", "pub_date", "was_published_recently"]
    # was_published_recently() 메소드를 추가
    
    # 29관리자 변경 목록(change list) 커스터마이징 추가
    
    list_filter = ["pub_date"]
    
    # 29관리자 변경 목록(search_fields) 커스터마이징 추가
    search_fields = ["question_text"]

# 변경 목록 맨 위에 검색 창이 추가된다. 
# 검색어를 입력하면, 장고는 question_text 필드를 검색한다. 
# 원하는 만큼의 필드를 사용할 수 있다  
# 그것은 내부적으로 LIKE 쿼리를 사용하기 때문에 검색 필드의 수를 적당한 수로 제한하면 데이터베이스가 검색을 더 쉽게 할 수 있다.

# 이제 변경 목록이 자동 페이징 기능을 제공한다
# 기본값은 페이지 당 100 개의 항목을 표시한다. 
# 변경 목록 페이지내이션, 검색 상자, 필터, 날짜-계층구조, 그리고 컬럼-헤더-정렬 모두 함께 작동합니다.


admin.site.register(Question, QuestionAdmin)
