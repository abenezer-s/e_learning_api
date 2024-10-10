from django.urls import path
from .views import *

urlpatterns =[
    path('course/<str:name>/', CourseDetailAPIView.as_view()),
    path('course/create/', CourseCreateAPIView.as_view()),
    path('courses/', CourseListAPIView.as_view(), name='courses-api'),
    path('course/<int:pk>/update/', CourseUpdateAPIView.as_view()),
    path('course/<int:pk>/delete/', CourseDestroyAPIView.as_view()),
    
]