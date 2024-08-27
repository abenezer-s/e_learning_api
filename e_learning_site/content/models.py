from django.db import models
from django.contrib.auth.models import User
#from user.models import UserProfile
# Create your models here.

class Course(models.Model):
    owner = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='course_owner')
    name = models.CharField(max_length=150, blank=False)
    number_of_modules = models.DecimalField(default=0, max_digits=3, decimal_places=0)
    created_at = models.DateField(blank=False)

    def __str__(self) -> str:
        return self.name

class Program(models.Model):
    """
    Prgram consists of one or more courses. 
    """
    owner = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='program_owner')
    name = models.CharField(max_length=150, blank=False)
    number_of_courses = models.DecimalField(default=0, max_digits=3, decimal_places=0)
    courses = models.ManyToManyField(Course, blank= True, default=None)

    created_at = models.DateField(blank=False)
    def __str__(self) -> str:
        return self.name

class Module(models.Model):
    owner = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='module_owner')
    name = models.CharField(max_length=150, blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='under_course')
    created_at = models.DateField(blank=False)

    def __str__(self) -> str:
        return self.name

class Media(models.Model):
    owner = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='media_owner')
    file = models.FileField(upload_to='media/')
    description = models.CharField(max_length=255, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='module')
                                   
class Application(models.Model):
    owner = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='program_course_owner') #program/course owner
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learner')
    motivation_letter = models.TextField(max_length=600, blank=False)
    submitted_at = models.DateField(blank=False)
    program = models.ManyToManyField(Program, default=None)
    course =  models.ManyToManyField(Course, default=None)
    status = [
        ('accpeted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]
    
    state = models.CharField(max_length=20, choices=status)

