# Generated by Django 5.1 on 2024-10-05 09:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0017_test_created_at_test_module_alter_question_answer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='created_at',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='content.question'),
        ),
        migrations.AddField(
            model_name='question',
            name='created_at',
            field=models.DateField(blank=True, default=None),
        ),
        migrations.AddField(
            model_name='test',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.TextField(),
        ),
    ]