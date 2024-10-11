from rest_framework import serializers
from .models import *
from course.serializers import CourseSerialzer

class ProgramSerialzer(serializers.ModelSerializer):
    courses = CourseSerialzer(read_only=True, many=True)
    class Meta:
        model = Program
        fields = [
            "id",
            "owner",
            "name",
            "description",
            "number_of_courses",
            "complete_within",
            "duration",
            "courses"
        ]

class AddCourseSerializer(serializers.Serializer):
    course = serializers.CharField()
    program = serializers.CharField()