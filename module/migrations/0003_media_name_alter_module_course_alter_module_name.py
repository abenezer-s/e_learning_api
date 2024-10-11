# Generated by Django 5.1 on 2024-10-11 19:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_rename_decription_course_description'),
        ('module', '0002_rename_num_tests_module_num_quizs'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='name',
            field=models.CharField(default='file name', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_module', to='course.course'),
        ),
        migrations.AlterField(
            model_name='module',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]