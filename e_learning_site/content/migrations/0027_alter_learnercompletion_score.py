# Generated by Django 5.1 on 2024-10-05 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0026_alter_learnercompletion_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learnercompletion',
            name='score',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
    ]
