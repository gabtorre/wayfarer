# Generated by Django 3.1.2 on 2020-12-06 22:22

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_auto_20201206_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='header_image',
            field=cloudinary.models.CloudinaryField(blank=True, default='eat3x7tmegk7jvt4kpjo.jpg', max_length=255, null=True, verbose_name='Header Image'),
        ),
    ]
