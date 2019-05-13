# Generated by Django 2.2.1 on 2019-05-13 19:41

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0009_search_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='cities',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=[]),
        ),
        migrations.AddField(
            model_name='search',
            name='countries',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=[]),
        ),
        migrations.AddField(
            model_name='search',
            name='types',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=[]),
        ),
    ]
