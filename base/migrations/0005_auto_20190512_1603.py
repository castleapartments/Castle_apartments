# Generated by Django 2.2.1 on 2019-05-12 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20190512_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photo_main',
            field=models.ImageField(upload_to='profile_images/', verbose_name='img'),
        ),
    ]
