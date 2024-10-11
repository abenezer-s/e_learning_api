from django.db import models
from course.models import Category, Course
from django.contrib.auth.models import User

# Create your models here.
class Program(models.Model):
    """
    Prgram consists of one or more courses. 
    """
    owner = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='program_owner')
    name = models.CharField(max_length=150, blank=False, unique=True)
    description = models.TextField(default="default description")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=None)
    number_of_courses = models.DecimalField(default=0, max_digits=3, decimal_places=0)
    courses = models.ManyToManyField(Course, blank= True, default=None)
    duration = models.IntegerField(default=None)   #estimated number of weeks this program might take to fiinish
    complete_within = models.DecimalField(blank=False, max_digits=2, default=None, decimal_places=0)      #number of weeks a learner has to finish content

    created_at = models.DateField(blank=False)
    def __str__(self) -> str:
        return self.name