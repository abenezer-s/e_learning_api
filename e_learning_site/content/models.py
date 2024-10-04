from django.db import models
from django.contrib.auth.models import User
#from user.models import UserProfile
# Create your models here.

class Course(models.Model):
    owner = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='course_owner')
    name = models.CharField(max_length=150, blank=False)
    number_of_modules = models.DecimalField(default=0, max_digits=3, decimal_places=0)
    created_at = models.DateField(blank=False)
    complete_within = models.DecimalField(blank=False, max_digits=2, default=None, decimal_places=0)      #number of weeks a learner has to finish content
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
    complete_within = models.DecimalField(blank=False, max_digits=2, default=None, decimal_places=0)      #number of weeks a learner has to finish content

    created_at = models.DateField(blank=False)
    def __str__(self) -> str:
        return self.name

class Module(models.Model):
    owner = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='module_owner')
    name = models.CharField(max_length=150, blank=False)
    content = models.TextField(default="default content", blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='under_course')
    created_at = models.DateField(blank=False)


    def __str__(self) -> str:
        return self.name

class Media(models.Model):
    owner = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='media_owner')
    file = models.FileField(upload_to='media/')
    description = models.CharField(max_length=255, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='module_media')
                                   
class Application(models.Model):
    owner = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='program_course_owner') #program/course owner
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learner')
    motivation_letter = models.TextField(max_length=600, blank=False)
    submitted_at = models.DateField(blank=False)
    program = models.ManyToManyField(Program, default=None)
    course =  models.ManyToManyField(Course, default=None)
    status = [
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]
    
    state = models.CharField(max_length=20, default=None, choices=status)

class Test(models.Model):
    """
    a model to store tests for a module with optional time limits.
    """
    module = models.ForeignKey(Module, on_delete=models.CASCADE, default=None)
    description = models.TextField(blank=False)
    time_limit = models.DecimalField(default=None, blank=True, max_digits=3, decimal_places=0)
    pass_score = models.DecimalField(default=50, blank=True, max_digits=3, decimal_places=0)
    created_at = models.DateField(blank=True, default=None)

class Answer(models.Model):
    """
    potential answer to a question
    """
    choice_number = models.DecimalField(default=None, blank=False, max_digits=1, decimal_places=0)
    value = models.TextField(blank=False)
    
class  Question(models.Model):
    """
    A model used to model a question which is part of the test model. 
    Must have muliple potetnial answers if question is multiple choice( multi=True)
    """
    test = models.ForeignKey(Test, default=None, on_delete=models.CASCADE, related_name='test_question')
    multi = models.BooleanField(blank=False)     #feild to determine wheter the wuerstion is multiple choice or fill in blank
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE, related_name='choices') 

class LearnerCompletion(models.Model):
    """
    Model to keep track of a learner's completion of programs and courses.
    Therefore making them eligible for a certificate if in this model
    """
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, null=True,default=None, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True,default=None, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, null=True,default=None, on_delete=models.CASCADE)
    completed_at = models.DateField()