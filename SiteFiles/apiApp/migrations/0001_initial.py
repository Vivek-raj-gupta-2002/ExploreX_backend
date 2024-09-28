# Generated by Django 5.1.1 on 2024-09-28 12:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('good_habit_1', models.CharField(blank=True, max_length=100, null=True)),
                ('good_habit_2', models.CharField(blank=True, max_length=100, null=True)),
                ('good_habit_3', models.CharField(blank=True, max_length=100, null=True)),
                ('good_habit_4', models.CharField(blank=True, max_length=100, null=True)),
                ('good_habit_5', models.CharField(blank=True, max_length=100, null=True)),
                ('bad_habit_1', models.CharField(blank=True, max_length=100, null=True)),
                ('bad_habit_2', models.CharField(blank=True, max_length=100, null=True)),
                ('bad_habit_3', models.CharField(blank=True, max_length=100, null=True)),
                ('bad_habit_4', models.CharField(blank=True, max_length=100, null=True)),
                ('bad_habit_5', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]