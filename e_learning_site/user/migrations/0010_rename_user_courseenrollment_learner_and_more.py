# Generated by Django 5.1 on 2024-08-27 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_remove_programenrollment_number_of_courses_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseenrollment',
            old_name='user',
            new_name='learner',
        ),
        migrations.RemoveField(
            model_name='courseenrollment',
            name='number_of_modules',
        ),
        migrations.RemoveField(
            model_name='courseenrollment',
            name='state',
        ),
        migrations.RemoveField(
            model_name='programenrollment',
            name='state',
        ),
    ]