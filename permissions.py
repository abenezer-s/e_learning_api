from rest_framework.permissions import BasePermission
from django.http import HttpResponse

class IsContentCreator(BasePermission):
    """
    Custom permission to only allow content creators to access the view.
    """
    def has_permission(self, request, view):
        try:
            return request.user.userprofile.creator
        except AttributeError:
            return HttpResponse('User is not a content creator', status=403)

class IsLearner(BasePermission):
    """
    Custom permission to only allow learners to access the view.
    """
    def has_permission(self, request, view):
        try:
            return not request.user.userprofile.creator
        except AttributeError:
            return HttpResponse('User is not a learner', status=403)

