# Generated by Django 5.1 on 2024-08-26 17:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_alter_course_created_at_alter_module_created_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='user',
        ),
        migrations.AddField(
            model_name='application',
            name='learner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='learner', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='program_course_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]