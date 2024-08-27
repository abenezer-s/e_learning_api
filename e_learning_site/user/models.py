from django.db import models
from django.contrib.auth.models import User
from content.models import Course, Program
# Create your models here.

class UserProfile(models.Model):
    name = models.CharField(max_length=10, default="some name")
    image = models.ImageField(default='images/default.jpeg',upload_to='images/')
    courses = models.ManyToManyField(Course, default=None, through='CourseEnrollment')
    programs = models.ManyToManyField(Program, default=None, through='ProgramEnrollment')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    creator = models.BooleanField(default=False)

    def __str__(self):
        return (self.user.username)
    
class ProgramEnrollment(models.Model):
    learner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    program = models.ForeignKey(Program,on_delete=models.CASCADE)
    number_of_courses_completed = models.DecimalField(default=0, max_digits=3, decimal_places=1)
    date_of_enrollment = models.DateField()
    progress = models.DecimalField(default=0,  max_digits=3, decimal_places=1)

class CourseEnrollment(models.Model):
    learner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    number_of_modules_completed = models.DecimalField(default=0, max_digits=3, decimal_places=1)
    date_of_enrollment = models.DateField()
    progress = models.DecimalField(default=0,  max_digits=3, decimal_places=1)