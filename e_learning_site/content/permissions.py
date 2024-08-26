from rest_framework.permissions import BasePermission
from django.http import HttpResponse
class IsContentCreator(BasePermission):
    
    def has_permission(self, request, view):
        try:
            return request.user.userprofile.creator
        except:
            return HttpResponse('usr is superuser')

class IsLearner(BasePermission):
    
    def has_permission(self, request, view):
        try:
            return not (request.user.userprofile.creator)
        except:
            return HttpResponse('usr is superuser')

