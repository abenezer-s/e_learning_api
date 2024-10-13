from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from .models import *

class AnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Answer
        fields = [
            'id',
           'question_id',
           'choice_number',
           'value',
        ]

        read_only_field = ['question_id']

class QuestionSerializer(serializers.ModelSerializer):
    
    choices = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields =[
            "id",
            "quiz",
            "value",
            "multi",
            "answer",
            "choices"
        ]

        read_only_field = ['quiz']

    def to_representation(self, instance):
    
        representation = super().to_representation(instance)
        
        user = self.context['request'].user
        
        # Check if the user is a creater, if so then 
        if not user.userprofile.creator:
            # Remove the field from representation
            representation.pop('answer', None)
        
        return representation
    
    def get_choices(self, obj):
        #return the available choices for a question if the question is multiple choice.
        if obj.multi:
            return AnswerSerializer(obj.choices.all(), read_only=True, many=True).data
        else:
            return None

class QuizSerialzer(serializers.ModelSerializer):
    quiz_question = QuestionSerializer(read_only=True, many=True)
    class Meta:
        model = Quiz
        fields =[
            "owner",
            "id",
            "module",
            "name",
            "description",
            "pass_score",
            "quiz_question",
        ]

        read_only_field = ['owner', 'module']