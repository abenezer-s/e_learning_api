from django.urls import path
from .views import *

urlpatterns = [   
    path('program/<str:name>/', ProgramDetailAPIView.as_view()),
    path('create/program/', ProgramCreateAPIView.as_view()),
    path('programs/', ProgramListAPIView.as_view()),
    path('program/<int:pk>/update/', ProgramUpdateAPIView.as_view()),
    path('program/<int:pk>/delete/', ProgramDestroyAPIView.as_view()),
]