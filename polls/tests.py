import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question
from django.urls import reverse


class QuestionModelTests(TestCase):
    # 테스트클래스에 상단에 임포트한 테스트를 상속시킴
    def test_was_published_recently_with_future_question(self):
        # 함수이름 앞머리 test로 시작해야함
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        # 시간은 현재시간에 30일을 더함
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        # 30일을 더한 질문생성하고 질문이 최근이냐고 호출하면 False가 나오게함


#미래의 pub_date를 가진 Question 인스턴스를 생성하는 메소드를 가진 django.test.TestCase 하위 클래스를 생성했다.
# 그런 다음 was_published_recently()의 출력이 False가 되는지 확인했다.

# 20 보다 포괄적인 테스트 추가
def test_was_published_recently_with_old_question(self):
    """
    was_published_recently() returns False for questions whose pub_date
    is older than 1 day.
    """
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_question = Question(pub_date=time)
    self.assertIs(old_question.was_published_recently(), False)
    # 하루가 넘어갔을때 False


def test_was_published_recently_with_recent_question(self):
    """
    was_published_recently() returns True for questions whose pub_date
    is within the last day.
    """
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_question = Question(pub_date=time)
    self.assertIs(recent_question.was_published_recently(), True)
# 하루가 넘어가지 않았을때 True


# 23. 새로운 뷰 테스트추가
def create_question(question_text, days):
    """
  질문 생성 함수인 create_question은 테스트 과정 중 설문을 생성하는 부분에서 반복 사용
  create_question을 호출하면 주어진 텍스트와 날짜 오프셋을 기반으로 한 새로운 질문이 생성되고 데이터베이스에 저장된다.

  주어진 `question_text`와 `days`만큼 현재 날짜를 기준으로 한 날짜 오프셋으로
    질문을 생성
    `days`가 음수이면 과거에 발행된 질문을 나타내며
    양수이면
    아직 발행되지 않은 미래의 질문을 나타낸다.
    """
    time = timezone.now() + datetime.timedelta(days=days)
     # 현재 날짜에서 `days`만큼의 시간 간격을 더하여 새로운 시간을 계산
       
    return Question.objects.create(question_text=question_text, pub_date=time)
   # Django의 ORM을 사용하여
   # Question 모델의 create 메서드를 사용하여 질문 생성 새로운 인스턴스를 생성하고 데이터베이스에 저장


class QuestionIndexViewTests(TestCase):
    
    def test_no_questions(self):
        """
      ``test_no_questions``는 데이터가 없는 경우
      질문을 생성하지 않지만 “No polls are available.” 메시지를 확인하고 ``latest_question_list``가 비어있는지 확인한다.
      
      Django의 TestCase 클래스를 사용하여 Question 모델의 인덱스 뷰에 대한 테스트를 정의하고 있다. 특히, "No questions exist" 상황에 대한 테스트 케이스를 구현하고 있다.
      
      django.test.TestCase 클래스는 몇가지 추가적인 선언 메소드를 제공하니 유의해야한다. 
      이 중에서  
      :meth:`~django.test.SimpleTestCase.assertContains() 와 
      :meth:`~django.test.TransactionTestCase.assertQuerySetEqual()`을 사용한다.
        """
        response = self.client.get(reverse("polls:index"))
        # polls:index URL에 대한 테스트클라이언트가 GET 요청을 수행하여 뷰를 호출한다.
        # response를 받아서 원하는 결과가 나오는지 확인
        
        self.assertEqual(response.status_code, 200)
        # 답의 상태 코드가 200인지 확인하여 요청이 성공했는지 확인한다.(Equal)
        
        self.assertContains(response, "No polls are available.")
        # Contains포함되어있나
        # 응답 내용에 "No polls are available." 메시지가 포함되어 있는지 확인한다.
        
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
        # 뷰의 context에서 latest_question_list가 빈 리스트인지 확인한다.
        
        # QuerySetEqual:self 테스트메서드를 이용해서 테스트를 한다
        
        # "No questions exist" 상황에 대한 뷰의 동작을 검증한다. 
        
        # 뷰가 정상적으로 동작하면서 사용자에게 "No polls are available."라는 메시지를 표시하고, latest_question_list가 빈 리스트인지를 확인한다.

    
    def test_past_question(self):
        """
        Django의 TestCase 클래스를 사용하여 Question 모델의 인덱스 뷰에 대한 테스트 케이스를 추가로 정의하고 있다. 
        "과거의 질문"에 대한 테스트를 수행한다.
        
        과거에 발행된 질문이 인덱스 페이지에 올바르게 표시되는지를 검증한다. 
        특히, 뷰가 과거에 발행된 질문을 가져오고 이를 latest_question_list에 올바르게 담아서 전달하는지를 확인한다.
        """
        question = create_question(question_text="Past question.", days=-30)
        # 현재 날짜로부터 30일 이전의 날짜에 발행된 "Past question."이라는 텍스트를 가진 Question 객체를 생성한다.
        
        response = self.client.get(reverse("polls:index"))
        # polls:index URL에 대한 GET 요청을 수행하여 뷰를 호출한다.
        
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )
        # 뷰의 컨텍스트에서 latest_question_list가 [question]와 같은지를 확인한다.

    
    
    def test_future_question(self):
        """
       Django의 TestCase 클래스를 사용하여 Question 모델의 인덱스 뷰에 대한 "미래의 질문"에 대한 테스트를 수행한다.
       
       미래에 발행될 질문이 인덱스 페이지에 표시되지 않아야 함을 검증한다. 
       데이터가 표시되면 오류
       
       따라서 "No polls are available." 메시지가 표시되어야 하고, latest_question_list가 빈 리스트인지를 확인한다.
        """
        create_question(question_text="Future question.", days=30)
        # 현재 날짜로부터 30일 이후의 날짜에 발행될 "Future question."이라는 텍스트를 가진 Question 객체를 생성한다.
        
        response = self.client.get(reverse("polls:index"))
        # polls:index URL에 대한 GET 요청을 수행하여 뷰를 호출한다.
        
        self.assertContains(response, "No polls are available.")
        # 응답 내용에 "No polls are available." 메시지가 포함되어 있는지 확인한다.
        
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
        # 뷰의 컨텍스트에서 latest_question_list가 빈 리스트인지를 확인한다.

    
    
    
    def test_future_question_and_past_question(self):
        """
        TestCase 클래스를 사용하여 Question 모델의 인덱스 뷰에 "과거의 질문"과 "미래의 질문"이 동시에 존재하는 경우에 대한 테스트를 수행한다.
        
        # 과거데이터만 표시되어야함
        """
        question = create_question(question_text="Past question.", days=-30)
        # 현재 날짜로부터 30일 이전의 날짜에 발행된 "Past question."이라는 텍스트를 가진 Question 객체를 생성한다.
        
        create_question(question_text="Future question.", days=30)
        # 현재 날짜로부터 30일 이후의 날짜에 발행될 "Future question."이라는 텍스트를 가진 Question 객체를 생성한다.
        
        response = self.client.get(reverse("polls:index"))
        # polls:index URL에 대한 GET 요청을 수행하여 뷰를 호출한다.
        
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )
        # 뷰의 컨텍스트에서 latest_question_list가 [question]와 같은지를 확인한다.
        
        # 과거에 발행된 질문과 미래에 발행될 질문이 동시에 존재할 때, 인덱스 페이지에는 과거의 질문만 표시되어야 함을 검증한다. 따라서 latest_question_list가 [question]와 같아야 한다.

    
    
    
    def test_two_past_questions(self):
        """
        Django의 TestCase 클래스를 사용하여 Question 모델의 인덱스 뷰에 대한 "과거의 질문"이 여러 개일 때에 대한 테스트를 수행한다.
        
        과거에 발행된 여러 질문이 인덱스 페이지에 올바르게 표시되는지를 검증한다. 
        따라서 latest_question_list가 [question2, question1]와 같아야 한다.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        # 현재 날짜로부터 30일 이전의 날짜에 발행된 "Past question 1."이라는 텍스트를 가진 Question 객체를 생성한다.
        
        question2 = create_question(question_text="Past question 2.", days=-5)
        # 현재 날짜로부터 5일 이전의 날짜에 발행된 "Past question 2."이라는 텍스트를 가진 Question 객체를 생성한다.
        
        response = self.client.get(reverse("polls:index"))
        # polls:index URL에 대한 GET 요청을 수행하여 뷰를 호출한다.
        
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )
        # 뷰의 컨텍스트에서 latest_question_list가 [question2, question1]와 같은지를 확인한다.
        


# 24.DetailView 테스트하기 추가
       
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """Django의 TestCase 클래스를 사용하여 Question 모델의 디테일 뷰에 대한 "미래의 질문"에 대한 상황을 검증한다.
        
        미래에 발행될 예정인 질문에 대한 디테일 뷰 호출 시, HTTP 응답 상태 코드가 404인지를 확인하여 해당 질문이 존재하지 않는다고 기대한다.
        """ 
        
        future_question = create_question(question_text="Future question.", days=5)
        # 현재 날짜로부터 5일 이후의 날짜에 발행될 "Future question."이라는 텍스트를 가진 Question 객체를 생성한다.
        
        url = reverse("polls:detail", args=(future_question.id,))
        # polls:detail URL에 대한 reverse 함수를 사용하여 future_question의 ID를 포함한 URL을 생성한다.
        
        response = self.client.get(url)
        # 생성된 URL에 대한 GET 요청을 수행하여 디테일 뷰를 호출한다.
        
        self.assertEqual(response.status_code, 404)
        # 응답의 상태 코드가 404인지를 확인한다.

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)  
        


