from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/', ModuleDetailAPIView.as_view()),
    path('create/<int:course_id>/', ModuleCreateAPIView.as_view()),
    path('', ModuleListAPIView.as_view()),
    path('<int:pk>/update/', ModuleUpdateAPIView.as_view()),
    path('<int:pk>/delete/', ModuleDestroyAPIView.as_view()),
    #media
    path('media/<int:pk>/', MediaDetailAPIView.as_view()),
    path('<int:module_id>/add-media/', MediaCreateAPIView.as_view()),
    path('medias/', MediaListAPIView.as_view()),
    path('media/<int:pk>/update/', MediaUpdateAPIView.as_view()),
    path('media/<int:pk>/delete/', MediaDestroyAPIView.as_view()),
    
    path('<int:module_id>/mark-complete/<int:learner_id>/', MarkComplete.as_view()),
]