# Generated by Django 2.1.5 on 2019-06-22 12:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0010_auto_20190622_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 22, 12, 44, 2, 347738, tzinfo=utc)),
        ),
    ]
