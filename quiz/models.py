from django.db import models
from module.models import Module
from django.contrib.auth.models import User
from course.models import Course
from program.models import Program

# Create your models here.
class Quiz(models.Model):
    """
    a model to store quizs for a module with optional time limits.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, default=None)
    description = models.TextField(blank=False)
    pass_score = models.DecimalField(default=50, blank=True, max_digits=3, decimal_places=0)
    num_of_questions = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    created_at = models.DateField(blank=True, default=None)
    
class  Question(models.Model):
    """
    A model used to model a question which is part of the quiz model. 
    Must have muliple potetnial answers if question is multiple choice( multi=True)
    """
    quiz = models.ForeignKey(Quiz, default=None, on_delete=models.CASCADE, related_name='quiz_question')
    value = models.TextField(default=None, blank=False)
    multi = models.BooleanField(blank=False)     #feild to determine wheter the question is multiple choice or fill in blank
    answer = models.TextField(blank=False)
    created_at = models.DateField(blank=True, default=None)

class Answer(models.Model):
    """
    potential answer to a question
    """
    choice_number = models.DecimalField(default=None, blank=False, max_digits=1, decimal_places=0)
    value = models.TextField(blank=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', default=None)
    created_at = models.DateField(default=None)

class Grade(models.Model):
    """
    model to store grades of learners.
    """
    module =  models.ForeignKey(Module, default=None, on_delete=models.CASCADE, related_name='module_grade')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_grade', blank=True, null=True)
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learner_grade')
    grade = models.DecimalField(blank=False, max_digits=5, decimal_places=2)
    passed = models.BooleanField(default=None)

class LearnerAnswer(models.Model):
    """
    model to keep track of learner answers.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()
    correct = models.BooleanField()
    
