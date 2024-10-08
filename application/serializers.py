from rest_framework import serializers
from .models import *

class ApplySerializer(serializers.Serializer):
    learner = serializers.CharField()
    motivation_letter = serializers.CharField()
    program_name = serializers.CharField()
    course_name = serializers.CharField()

class ApplicationResponseSerializer(serializers.Serializer):
    learner = serializers.CharField()
    program_name = serializers.CharField()
    course_name = serializers.CharField()
    response = serializers.CharField()

class ApplicationSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'