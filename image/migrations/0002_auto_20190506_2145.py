# Generated by Django 2.2.1 on 2019-05-06 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='imageURL',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
