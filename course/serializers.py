from rest_framework import serializers
from .models import *
from module.serializers import ModuleSerialzer

class CourseSerialzer(serializers.ModelSerializer):
    course_module = ModuleSerialzer(read_only=True, many=True)
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
            "course_module",
        ]
        read_only_fields = ['number_of_modules']

class CategorySerialzer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'