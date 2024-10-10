from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/', ApplicationDetailAPIView.as_view()),
    path('create/', ApplicationCreateAPIView.as_view()),
    path(' ', ApplicationListAPIView.as_view()),
    path('respond/', ApplicationResponse.as_view()),
    path('<int:pk>/update/', ApplicationUpdateAPIView.as_view()),
    path('<int:pk>/delete/', ApplicationDestroyAPIView.as_view()),
    path('apply/', Apply.as_view()),
]