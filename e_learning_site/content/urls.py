from django.urls import path
from .views import *
urlpatterns = [
    path('program/<str:name>/', ProgramDetailAPIView.as_view()),
    path('course/<str:name>/', CourseDetailAPIView.as_view()),
    path('module/<str:name>/', ModuleDetailAPIView.as_view()),
    path('media/<int:pk>/', MediaDetailAPIView.as_view()),
    path('application/<int:pk>/', ApplicationDetailAPIView.as_view()),

    path('create/program/', ProgramCreateAPIView.as_view()),
    path('add/course/', AddCourseAPIView.as_view(), name='add-course-view'),
    path('create/course/', CourseCreateAPIView.as_view()),
    path('create/module/', ModuleCreateAPIView.as_view()),
    path('media/create/', MediaCreateAPIView.as_view()),
    path('application/create/', ApplicationCreateAPIView.as_view()),
    path('apply/', Apply.as_view()),
    path('mark_complete/', MarkComplete.as_view()),

    path('programs/', ProgramListAPIView.as_view()),
    path('courses/', CourseListAPIView.as_view(), name='courses-api'),
    path('modules/', ModuleListAPIView.as_view()),
    path('medias/', MediaListAPIView.as_view()),
    path('applications/', ApplicationListAPIView.as_view()),
    path('applications/respond', ApplicationResponse.as_view()),


    path('program/<int:pk>/update/', ProgramUpdateAPIView.as_view()),
    path('course/<int:pk>/update/', CourseUpdateAPIView.as_view()),
    path('module/<int:pk>/update/', ModuleUpdateAPIView.as_view()),
    path('media/<int:pk>/update/', MediaUpdateAPIView.as_view()),
    path('application/<int:pk>/update/', ApplicationUpdateAPIView.as_view()),

    path('program/<int:pk>/delete/', ProgramDestroyAPIView.as_view()),
    path('course/<int:pk>/delete/', CourseDestroyAPIView.as_view()),
    path('module/<int:pk>/delete/', ModuleDestroyAPIView.as_view()),
    path('media/<int:pk>/delete/', MediaDestroyAPIView.as_view()),
    path('application/<int:pk>/delete/', ApplicationDestroyAPIView.as_view()),

]