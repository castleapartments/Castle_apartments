# Generated by Django 2.2.1 on 2019-05-11 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
