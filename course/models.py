from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    """
    category for courses and programs
    """
    name = models.CharField(max_length=30, blank=False)

class Course(models.Model):
    owner = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='course_owner')
    name = models.CharField(max_length=150, blank=False, unique=True)
    number_of_modules = models.DecimalField(default=0, max_digits=3, decimal_places=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=None)
    created_at = models.DateField(blank=False)
    duration = models.IntegerField(default=None)   #estimated number of weeks this course might take to fiinish
    complete_within = models.DecimalField(blank=False, max_digits=2, default=None, decimal_places=0)      #number of weeks a learner has to finish content
    def __str__(self) -> str:
        return self.name