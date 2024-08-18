from django.db import models
from django.contrib.auth.models import User
#from content.models import Course, Program
# Create your models here.

class UserProfile(models.Model):

    image = models.ImageField(default='/images/default.jpeg',upload_to='images/')
    roles = [
        ('m','content_manager'),
        ('c','content_consumer')
    ]
    role = models.CharField(max_length=10, choices=roles)
    #courses = models.ManyToManyField(Course, default=None, through='CourseEnrollment')
    #programs = models.ManyToManyField(Program, default=None, through='ProgramEnrollment')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return (self.user.username)