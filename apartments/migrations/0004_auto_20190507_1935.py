# Generated by Django 2.2.1 on 2019-05-07 19:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apartments', '0003_auto_20190506_2145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='user',
        ),
        migrations.AddField(
            model_name='apartment',
            name='owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
