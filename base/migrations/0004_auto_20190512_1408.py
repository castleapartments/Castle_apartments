# Generated by Django 2.2.1 on 2019-05-12 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20190512_1358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='profile_image',
            new_name='photo_main',
        ),
    ]
