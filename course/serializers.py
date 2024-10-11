from rest_framework import serializers
from .models import *

class CourseSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "id",
            "owner",
            "name",
            "description",
            "number_of_modules",
            "complete_within",
            "category",
            "duration",
        ]

class CategorySerialzer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'