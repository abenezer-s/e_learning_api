from django.urls import path
from .views import *
urlpatterns = [
    path('<int:pk>/', QuizDetailAPIView.as_view()),
    path('create/<int:module_id>/', QuizCreateAPIView.as_view()),
    path('', QuizListAPIView.as_view()),
    path('<int:pk>/update/', QuizUpdateAPIView.as_view()),
    path('<int:pk>/delete/', QuizDestroyAPIView.as_view()),
    
    path('question/<int:pk>/', QuestionDetailAPIView.as_view()),
    path('<int:quiz_id>/add-question/', QuestionCreateAPIView.as_view()),
    path('question/<int:pk>/update/', QuestionUpdateAPIView.as_view()),
    path('question/<int:pk>/delete/', QuestionDestroyAPIView.as_view()),
    path('<int:quiz_id>/submit/<int:learner_id>/', SubmitAnswersAPIView.as_view(), name='submit-quiz'),
    
    path('answer/<int:pk>/', AnswerDetailAPIView.as_view()),
    path('question/<int:question_id>/add-answer/', AnswerCreateAPIView.as_view()),
    path('answer/<int:pk>/update/', AnswerUpdateAPIView.as_view()),
    path('answer/<int:pk>/delete/', AnswerDestroyAPIView.as_view()),
]