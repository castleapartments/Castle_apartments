# Generated by Django 2.2.1 on 2019-05-06 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0003_auto_20190506_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='imageURL',
            field=models.ImageField(blank=True, unique=True, upload_to='media/'),
        ),
    ]