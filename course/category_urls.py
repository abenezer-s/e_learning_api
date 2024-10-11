from django.urls import path
from .views import *

urlpatterns =[
    path('create/', CategoryCreateAPIView.as_view()),
    path('', CategoryListAPIView.as_view(), name='categories-api'),
    path('<int:pk>/', CategoryDetailAPIView.as_view()),
    path('<int:pk>/update/', CategoryUpdateAPIView.as_view()),
    path('<int:pk>/delete/', CategoryDestroyAPIView.as_view()),
]