# Generated by Django 5.1 on 2024-08-24 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_remove_userprofile_role'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='creater',
            new_name='creator',
        ),
    ]