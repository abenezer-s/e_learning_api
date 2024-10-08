from django.urls import path
from .views import *

urlpatterns = [
    path('module/<int:pk>/', ModuleDetailAPIView.as_view()),
    path('create/module/', ModuleCreateAPIView.as_view()),
    path('module/<int:module_id>/mark_complete/<int:learner_id>/', MarkComplete.as_view()),
    path('modules/', ModuleListAPIView.as_view()),
    path('module/<int:pk>/update/', ModuleUpdateAPIView.as_view()),
    path('module/<int:pk>/delete/', ModuleDestroyAPIView.as_view()),
    path('media/<int:pk>/', MediaDetailAPIView.as_view()),
    path('create/media/', MediaCreateAPIView.as_view()),
    path('upload/', AddMedia.as_view(), name='upload-api'),
    path('medias/', MediaListAPIView.as_view()),
    path('media/<int:pk>/update/', MediaUpdateAPIView.as_view()),
    path('media/<int:pk>/delete/', MediaDestroyAPIView.as_view()),
    path('upload/', AddMedia.as_view(), name='upload-api'),
]