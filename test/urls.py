from django.urls import path
from .views import *
urlpatterns = [
    path('test/<int:pk>/', TestDetailAPIView.as_view()),
    path('create/test/', TestCreateAPIView.as_view()),
    path('tests/', TestListAPIView.as_view()),
    path('test/<int:pk>/update/', TestUpdateAPIView.as_view()),
    path('test/<int:pk>/delete/', TestDestroyAPIView.as_view()),
    #submit answers for a test
    path('tests/<int:test_id>/submit/<int:learner_id>/', SubmitAnswersAPIView.as_view(), name='submit-test'),
    path('question/<int:pk>/', QuestionDetailAPIView.as_view()),
    path('create/question/', QuestionCreateAPIView.as_view()),
    path('question/<int:pk>/update/', QuestionUpdateAPIView.as_view()),
    path('question/<int:pk>/delete/', QuestionDestroyAPIView.as_view()),
    path('answer/<int:pk>/', AnswerDetailAPIView.as_view()),
    path('create/answer/', AnswerCreateAPIView.as_view()),
    path('answer/<int:pk>/update/', AnswerUpdateAPIView.as_view()),
    path('answer/<int:pk>/delete/', AnswerDestroyAPIView.as_view()),
]