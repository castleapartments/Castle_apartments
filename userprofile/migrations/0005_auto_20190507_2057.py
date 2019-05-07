# Generated by Django 2.2.1 on 2019-05-07 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_auto_20190507_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='creditCardNameOnCard',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='creditCardProvider',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='firstName',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lastName',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='sex',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female')], default='Male', max_length=15),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='ssn',
            field=models.CharField(blank=True, default='', max_length=150, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='streetName',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
    ]
