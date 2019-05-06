# Generated by Django 2.2.1 on 2019-05-06 20:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('location', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(default='Male', max_length=5)),
                ('firstName', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('lastName', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('email', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('phone', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('ssn', models.IntegerField(blank=True, default='', null=True)),
                ('streetName', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('streetNumber', models.IntegerField(blank=True, default='', null=True)),
                ('postalCode', models.IntegerField(blank=True, default='', null=True)),
                ('creditCardNumber', models.IntegerField(blank=True, default='', null=True)),
                ('creditCardSecurityNumber', models.IntegerField(blank=True, default='', null=True)),
                ('creditCardNameOnCard', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('creditCardExpiry', models.DateField(blank=True, null=True)),
                ('cityID', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.PROTECT, to='location.City')),
                ('countryID', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.PROTECT, to='location.Country')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]