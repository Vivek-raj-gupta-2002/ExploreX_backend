# Generated by Django 5.1.1 on 2024-10-21 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiApp', '0007_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepic',
            name='image',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
