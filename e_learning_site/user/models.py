from django.db import models
from django.contrib.auth.models import User
from content.models import Course, Program
# Create your models here.

class UserProfile(models.Model):
    name = models.CharField(max_length=10, default="some name")
    image = models.ImageField(default='images/default.jpeg',upload_to='images/')
    roles = [
        ('m','content_manager'),
        ('c','content_consumer')
    ]
    role = models.CharField(max_length=10, default='c',choices=roles)
    courses = models.ManyToManyField(Course, default=None, through='CourseEnrollment')
    programs = models.ManyToManyField(Program, default=None, through='ProgramEnrollment')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return (self.user.username)
    
class ProgramEnrollment(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    program = models.ForeignKey(Program,on_delete=models.CASCADE)
    number_of_courses = models.DecimalField(default=0, max_digits=3, decimal_places=0)
    number_of_courses_completed = models.DecimalField(default=0, max_digits=3, decimal_places=1)
    date_of_enrollment = models.DateField()
    status = [
        ('accpeted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]

    state = models.CharField(max_length=8, choices=status)
    progress = models.DecimalField(default=0,  max_digits=3, decimal_places=1)

class CourseEnrollment(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    number_of_modules = models.DecimalField(default=0, max_digits=3, decimal_places=0)
    number_of_modules_completed = models.DecimalField(default=0, max_digits=3, decimal_places=1)
    date_of_enrollment = models.DateField()
    status = [
        ('accpeted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]

    state = models.CharField(max_length=8, choices=status)
    progress = models.DecimalField(default=0,  max_digits=3, decimal_places=1)