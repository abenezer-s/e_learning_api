from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/', ApplicationDetailAPIView.as_view()),
    path('', ApplicationListAPIView.as_view()),
    path('<int:pk>/update/', ApplicationUpdateAPIView.as_view()),
    path('<int:pk>/delete/', ApplicationDestroyAPIView.as_view()),
    path('course/<int:course_id>/apply/<int:learner_id>/', ApplyCourse.as_view()),
    path('program/<int:program_id>/apply/<int:learner_id>/', ApplyProgram.as_view()),
    path('course/<int:course_id>/respond/<int:learner_id>/', ApplicationResponseCourse.as_view()),
    path('program/<int:program_id>/respond/<int:learner_id>/', ApplicationResponseProgram.as_view()),

]