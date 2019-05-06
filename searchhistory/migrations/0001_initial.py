# Generated by Django 2.2.1 on 2019-05-06 20:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchHistory',
            fields=[
                ('searchHistoryID', models.AutoField(primary_key=True, serialize=False)),
                ('searchValue', models.CharField(max_length=50)),
                ('searchFilter', models.CharField(max_length=50)),
                ('searchHistoryCreated', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
