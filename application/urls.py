from django.urls import path
from .views import *

urlpatterns = [
    path('application/<int:pk>/', ApplicationDetailAPIView.as_view()),
    path('create/application/', ApplicationCreateAPIView.as_view()),
    path('applications/', ApplicationListAPIView.as_view()),
    path('applications/respond', ApplicationResponse.as_view()),
    path('application/<int:pk>/update/', ApplicationUpdateAPIView.as_view()),
    path('application/<int:pk>/delete/', ApplicationDestroyAPIView.as_view()),
    path('apply/', Apply.as_view()),
]