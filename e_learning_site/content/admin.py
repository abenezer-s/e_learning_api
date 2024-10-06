from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Program)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Media) 
admin.site.register(Application)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Grade)
admin.site.register(LearnerAnswer)
admin.site.register(LearnerCompletion)


class LearnerCompletionAdmin(admin.ModelAdmin):
    actions = ['delete_selected']  # Ensures delete action is available




