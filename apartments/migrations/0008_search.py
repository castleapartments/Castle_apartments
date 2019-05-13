# Generated by Django 2.2.1 on 2019-05-12 23:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apartments', '0007_auto_20190512_1746'),
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('search_id', models.AutoField(primary_key=True, serialize=False)),
                ('min_size', models.IntegerField(null=True)),
                ('max_size', models.IntegerField(null=True)),
                ('min_rooms', models.IntegerField(null=True)),
                ('max_rooms', models.IntegerField(null=True)),
                ('min_price', models.IntegerField(null=True)),
                ('max_price', models.IntegerField(null=True)),
                ('street', models.CharField(blank=True, max_length=100)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('age', models.CharField(blank=True, choices=[('d', '1 Day'), ('w', '1 Week')], max_length=1)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
