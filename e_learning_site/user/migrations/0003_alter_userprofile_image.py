# Generated by Django 5.1 on 2024-08-18 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_userprofile_image_courseenrollment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='images/default.jpeg', upload_to='images/'),
        ),
    ]