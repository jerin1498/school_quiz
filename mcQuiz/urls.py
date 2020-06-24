from django.conf.urls import url
from .views import QuizList, QuizExam, SaveExamResult, ResultList


urlpatterns = [
    url(r'^$', QuizList.as_view(), name='quiz-list'),
    url(r'^(?P<slug>[\w-]+)/$', QuizExam.as_view(), name='exam'),
    url(r'^save', SaveExamResult.as_view(), name='save'),
    url(r'^result', ResultList.as_view(), name='result_list'),

]

