# Generated by Django 2.2.1 on 2019-05-06 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0002_auto_20190506_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='imageURL',
            field=models.ImageField(unique=True, upload_to=''),
        ),
    ]
