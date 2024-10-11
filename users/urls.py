from django.urls import path
from .views import *
urlpatterns = [
    path('sign-up/learner/', sign_up_learner, name='signup-consumer'),
    path('sign-up/creator/', sign_up_creator, name='signup-creator'),
    path('login/', LoginView.as_view(), name='login-view'),
    path('logout/', LogoutView.as_view(), name='logout-view'),

    path('profiles/', UserProfileListAPIView.as_view(), name='UserProfile-list-api-view'),
    path('<int:pk>/profile/', UserProfileDetailAPIView.as_view(), name='UserProfile-detail-api-view'),
    path('<int:pk>/edit/profile/',  UserProfileUpdateAPIView.as_view(), name='UserProfile-update-api-view'),
    #path('<int:pk>/delete/profile/',  UserProfileDestroyAPIView.as_view(), name='UserProfile-delete-api-view'),

    path('all/', UserListAPIView.as_view(), name='users-api'),
    path('<int:pk>/', UserDetailAPIView.as_view(), name='user-detail-api-view'),
    path('<int:pk>/edit/',  UserUpdateAPIView.as_view(), name='user-update-api-view'),
    path('<int:pk>/delete/',  UserDestroyAPIView.as_view(), name='user-delete-api-view'),

    path('program_enroll/<str:name>/', ProgramEnrollmentDetailAPIView.as_view()),
    path('course_enroll/<str:name>/', CourseEnrollmentDetailAPIView.as_view()),
]