# Generated by Django 5.1 on 2024-10-11 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_course_decription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='decription',
            new_name='description',
        ),
    ]
