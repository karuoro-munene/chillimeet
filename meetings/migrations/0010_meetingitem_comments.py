# Generated by Django 4.1.3 on 2022-11-23 18:19

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0009_meetingreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingitem',
            name='comments',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500, null=True), null=True, size=None),
        ),
    ]