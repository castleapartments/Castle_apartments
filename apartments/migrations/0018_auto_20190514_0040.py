# Generated by Django 2.2.1 on 2019-05-14 00:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0017_merge_20190513_2304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='photo_main',
        ),
        migrations.AddField(
            model_name='apartmentimages',
            name='primary',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='apartmentimages',
            name='apartment_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='apartments.Apartment'),
        ),
    ]
