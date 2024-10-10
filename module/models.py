from django.db import models
from django.contrib.auth.models import User
from course.models import Course
from program.models import Program

# Create your models here.
class Module(models.Model):
    owner = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='module_owner')
    name = models.CharField(max_length=150, blank=False)
    content = models.TextField(default="default content", blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='under_course')
    created_at = models.DateField(blank=False)
    num_quizs = models.DecimalField(decimal_places=0, max_digits=2, default=0)

    def __str__(self) -> str:
        return self.name

class Media(models.Model):
    owner = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='media_owner')
    file = models.FileField(upload_to='media/')
    description = models.CharField(max_length=255, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='module_media')

class LearnerCompletion(models.Model):
    """
    Model to keep track of a learner's completion of programs and courses.
    Therefore making them eligible for a certificate if in this model
    """
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, null=True,default=None, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True,default=None, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, null=True,default=None, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    completed_at = models.DateField()