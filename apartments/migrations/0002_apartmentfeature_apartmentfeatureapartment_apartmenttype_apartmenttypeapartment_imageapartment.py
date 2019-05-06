# Generated by Django 2.2.1 on 2019-05-06 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
        ('apartments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApartmentFeature',
            fields=[
                ('apartmentFeatureID', models.AutoField(primary_key=True, serialize=False)),
                ('apartmentFeatureName', models.CharField(max_length=50)),
                ('apartmentFeatureCreated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApartmentType',
            fields=[
                ('apartmentTypeID', models.AutoField(primary_key=True, serialize=False)),
                ('apartmentTypeName', models.CharField(max_length=50)),
                ('apartmentTypeCreated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImageApartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageApartmentCreated', models.DateTimeField(auto_now_add=True)),
                ('apartmentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apartments.Apartment')),
                ('imageID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='image.Image')),
            ],
        ),
        migrations.CreateModel(
            name='ApartmentTypeApartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apartmentTypeApartmentCreated', models.DateTimeField(auto_now_add=True)),
                ('apartmentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apartments.Apartment')),
                ('apartmentTypeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apartments.ApartmentType')),
            ],
        ),
        migrations.CreateModel(
            name='ApartmentFeatureApartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apartmentFeatureApartmentCreated', models.DateTimeField(auto_now_add=True)),
                ('apartmentFeatureID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apartments.ApartmentFeature')),
                ('apartmentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apartments.Apartment')),
            ],
        ),
    ]
