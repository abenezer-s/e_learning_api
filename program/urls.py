from django.urls import path
from .views import *

urlpatterns = [   
    path('<str:name>/', ProgramDetailAPIView.as_view()),
    path('create/', ProgramCreateAPIView.as_view()),
    path(' ', ProgramListAPIView.as_view()),
    path('<int:pk>/update/', ProgramUpdateAPIView.as_view()),
    path('<int:pk>/delete/', ProgramDestroyAPIView.as_view()),
]