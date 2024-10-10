from django.db import models
from course.models import Course
from program.models import Program
from django.contrib.auth.models import User

# Create your models here.
class Application(models.Model):
    owner = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='program_course_owner') #program/course owner
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learner')
    motivation_letter = models.TextField(max_length=600, blank=False)
    submitted_at = models.DateField(blank=False)
    program = models.ForeignKey(Program,default=None, on_delete=models.CASCADE)
    course =  models.ForeignKey(Course,default=None, on_delete=models.CASCADE)
    status = [
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]
    
    state = models.CharField(max_length=20, default=None, choices=status)
