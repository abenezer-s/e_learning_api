# Generated by Django 5.1 on 2024-10-06 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_courseenrollment_deadline_courseenrollment_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseenrollment',
            name='status',
            field=models.CharField(choices=[('in progress', 'In Progress'), ('completed', 'Completed'), ('incomplete', 'InComplete')], default='in porgress', max_length=11),
        ),
    ]
