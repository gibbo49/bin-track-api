# Generated by Django 3.2.23 on 2023-12-31 05:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BinObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bin_id', models.CharField(max_length=255)),
                ('bin_size', models.CharField(max_length=255)),
                ('bin_type', models.CharField(max_length=255)),
                ('bin_owner', models.CharField(max_length=255)),
                ('bin_location', models.CharField(max_length=255)),
                ('bin_defects', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
