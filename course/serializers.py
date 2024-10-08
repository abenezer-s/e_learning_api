from rest_framework import serializers
from .models import *

class CourseSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "owner",
            "name",
            "number_of_modules",
            "complete_within",
        ]