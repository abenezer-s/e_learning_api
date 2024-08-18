# Generated by Django 5.1 on 2024-08-18 14:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('number_of_modules', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('created_at', models.DateField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_modules', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('number_of_modules_completed', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('date_of_enrollment', models.DateField()),
                ('state', models.CharField(choices=[('accpeted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending')], max_length=8)),
                ('progress', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('created_at', models.DateField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='under_course', to='content.course')),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='media/')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='module', to='content.module')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('number_of_courses', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('created_at', models.DateField()),
                ('courses', models.ManyToManyField(to='content.course')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivation_letter', models.TextField(max_length=600)),
                ('submitted_at', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('course', models.ManyToManyField(default=None, to='content.course')),
                ('program', models.ManyToManyField(default=None, to='content.program')),
            ],
        ),
        migrations.CreateModel(
            name='ProgramEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_courses', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('number_of_courses_completed', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('date_of_enrollment', models.DateField()),
                ('state', models.CharField(choices=[('accpeted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending')], max_length=8)),
                ('progress', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.program')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile')),
            ],
        ),
    ]
