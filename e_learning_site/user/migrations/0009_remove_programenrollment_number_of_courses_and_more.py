# Generated by Django 5.1 on 2024-08-26 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_rename_creater_userprofile_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programenrollment',
            name='number_of_courses',
        ),
        migrations.AlterField(
            model_name='programenrollment',
            name='state',
            field=models.CharField(choices=[('accpeted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending')], default=None, max_length=8),
        ),
    ]
