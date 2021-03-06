# Generated by Django 2.2.1 on 2019-05-09 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('apartment_id', models.AutoField(primary_key=True, serialize=False)),
                ('add_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('street_name', models.CharField(default='', max_length=100)),
                ('street_number', models.CharField(default='', max_length=10)),
                ('postcode', models.CharField(default='', max_length=50)),
                ('city', models.CharField(default='', max_length=50)),
                ('country', models.CharField(default='', max_length=50)),
                ('size', models.IntegerField(default=0)),
                ('rooms', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('price', models.IntegerField(default=0)),
                ('approved', models.BooleanField(default=False)),
                ('approval_date', models.DateTimeField(blank=True, null=True)),
                ('sold', models.BooleanField(default=False)),
                ('sold_date', models.DateField(blank=True, null=True)),
                ('photo_main', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]
