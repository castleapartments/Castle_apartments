# Generated by Django 2.2.1 on 2019-05-12 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20190512_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photo_main',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
