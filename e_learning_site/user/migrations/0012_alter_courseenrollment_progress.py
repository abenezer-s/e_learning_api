# Generated by Django 5.1 on 2024-08-28 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_rename_user_programenrollment_learner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseenrollment',
            name='progress',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
    ]