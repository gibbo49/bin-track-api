# Generated by Django 3.2.23 on 2024-01-03 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20240102_0530'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
