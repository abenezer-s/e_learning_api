from django.db import models
from django.contrib.auth.models import User
#from user.models import UserProfile
# Create your models here.

class Course(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_owner')
    name = models.CharField(max_length=150, blank=False)
    number_of_modules = models.DecimalField(default=0, max_digits=3, decimal_places=0)
    created_at = models.DateField(blank=False)

    def __str__(self) -> str:
        return self.name

class Program(models.Model):
    """
    Prgram consists of one or more courses. 
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='program_owner')
    name = models.CharField(max_length=150, blank=False)
    number_of_courses = models.DecimalField(default=0, max_digits=3, decimal_places=0)
    courses = models.ManyToManyField(Course)

    created_at = models.DateField(blank=False)
    def __str__(self) -> str:
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=150, blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='under_course')
    created_at = models.DateField(blank=False)

    def __str__(self) -> str:
        return self.name

class Media(models.Model):
    file = models.FileField(upload_to='media/')
    description = models.CharField(max_length=255, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='module')
                                   
class Application(models.Model):
    motivation_letter = models.TextField(max_length=600, blank=False)
    submitted_at = models.DateField(blank=False)
    program = models.ManyToManyField(Program, default=None)
    course =  models.ManyToManyField(Course, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

#class ProgramEnrollment(models.Model):
#    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
#    program = models.ForeignKey(Program,on_delete=models.CASCADE)
#    number_of_courses = models.DecimalField(default=0, max_digits=3, decimal_places=0)
#    number_of_courses_completed = models.DecimalField(default=0, max_digits=3, decimal_places=1)
#    date_of_enrollment = models.DateField()
#    status = [
#        ('accpeted', 'Accepted'),
#        ('rejected', 'Rejected'),
#        ('pending', 'Pending'),
#    ]
#
#    state = models.CharField(max_length=8, choices=status)
#    progress = models.DecimalField(default=0,  max_digits=3, decimal_places=1)
#
#class CourseEnrollment(models.Model):
#    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
#    course = models.ForeignKey(Course,on_delete=models.CASCADE)
#    number_of_modules = models.DecimalField(default=0, max_digits=3, decimal_places=0)
#    number_of_modules_completed = models.DecimalField(default=0, max_digits=3, decimal_places=1)
#    date_of_enrollment = models.DateField()
#    status = [
#        ('accpeted', 'Accepted'),
#        ('rejected', 'Rejected'),
#        ('pending', 'Pending'),
#    ]
#
#    state = models.CharField(max_length=8, choices=status)
#    progress = models.DecimalField(default=0,  max_digits=3, decimal_places=1)