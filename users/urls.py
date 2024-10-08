from django.urls import path
from .views import *
urlpatterns = [
    path('consumer_sign-up/', content_consumer_sign_up, name='signup-consumer'),
    path('creator_sign-up/', content_creator_sign_up, name='signup-creator'),
    path('login/', LoginView.as_view(), name='login-view'),
    path('logout/', LogoutView.as_view(), name='logout-view'),

    path('', UserProfileListAPIView.as_view(), name='UserProfile-list-api-view'),
    path('<int:pk>/', UserProfileDetailAPIView.as_view(), name='UserProfile-detail-api-view'),
    path('<int:pk>/edit/',  UserProfileUpdateAPIView.as_view(), name='UserProfile-update-api-view'),
    path('<int:pk>/delete/',  UserProfileDestroyAPIView.as_view(), name='UserProfile-delete-api-view'),

    path('users/', UserListAPIView.as_view(), name='users-api'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail-api-view'),
    path('users/<int:pk>/edit/',  UserUpdateAPIView.as_view(), name='user-update-api-view'),
    path('users/<int:pk>/delete/',  UserDestroyAPIView.as_view(), name='user-delete-api-view'),

    path('program_enroll/<str:name>/', ProgramEnrollmentDetailAPIView.as_view()),
    path('course_enroll/<str:name>/', CourseEnrollmentDetailAPIView.as_view()),
]