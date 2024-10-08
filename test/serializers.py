from rest_framework import serializers
from .models import *

class AnswerSerializer(serializers.ModelSerializer):
     question_id = serializers.CharField(write_only=True)
     class Meta:
         model = Answer
         fields = [
            'choice_number',
            'value',
            'question_id'
         ]

class QuestionSerializer(serializers.ModelSerializer):
    answer = serializers.CharField(write_only=True)
    choices = serializers.SerializerMethodField()
    test_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = Question
        fields =[
            "id",
            "test_id",
            "value",
            "multi",
            "answer",
            "choices"
        ]

    def get_choices(self, obj):
        if obj.multi:
            return AnswerSerializer(obj.choices.all(), read_only=True, many=True).data
        else:
            return None

class TestSerialzer(serializers.ModelSerializer):
    test_question = QuestionSerializer(read_only=True, many=True)
    module_id = serializers.CharField(write_only=True)
    class Meta:
        model = Test
        fields =[
            "id",
            "description",
            "time_limit",
            "pass_score",
            "module_id",
            "test_question"
        ]
