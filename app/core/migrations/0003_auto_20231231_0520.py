# Generated by Django 3.2.23 on 2023-12-31 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_binobject'),
    ]

    operations = [
        migrations.AddField(
            model_name='binobject',
            name='bin_tagged_out',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='binobject',
            name='special_bin',
            field=models.BooleanField(default=False),
        ),
    ]
