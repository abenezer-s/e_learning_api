from django.contrib import admin
from .models import UserProfile, CourseEnrollment, ProgramEnrollment
# Register your models here.

from django.contrib import admin
from django.utils.html import format_html

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('image_tag',)

    #def delete(self, obj):
    #    return format_html('<a href="{}" class="button">Delete</a>', obj.get_delete_url())
    #delete.short_description = 'Delete'
    def image_tag(self, obj):
        return format_html('<img src="{}" width="100" height="100" />'.format(obj.image.url))
    image_tag.short_description = 'Image'

admin.site.register(UserProfile, UserProfileAdmin,)
admin.site.register(CourseEnrollment)
admin.site.register(ProgramEnrollment)