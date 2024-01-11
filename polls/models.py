import datetime

from django.db import models
from django.utils import timezone
# 29.관리자 변경 목록(change list) 커스터마이징 추가
from django.contrib import admin


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text 
       
    # 19버그수정
    # def was_published_recently(self):
    #     return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    def was_published_recently(self):
     now = timezone.now()
     return now - datetime.timedelta(days=1) <= self.pub_date <= now
# timezone.now()를 사용하여 현재 시간을 가져온다.
# datetime.timedelta(days=1)을 사용하여 1일의 시간 간격을 생성
# now - datetime.timedelta(days=1)는 현재 날짜와 1일 전의 날짜를 계산
# self.pub_date는 해당 Question 객체의 발행일자(pub_date 필드)이다.
# self.pub_date가 1일 전의 날짜 이상이면서 현재 날짜 이하인지를 확인한다.
# 만약 조건이 참이면 True를 반환하고, 그렇지 않으면 False를 반환한다.
# Question 객체의 pub_date가 최근 24시간 이내에 있는지를 판단하여 그 결과를 불리언 값으로 반환한다.


# 29.관리자 변경 목록(change list) 커스터마이징 추가
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now 

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)   
    def __str__(self):
        return self.choice_text