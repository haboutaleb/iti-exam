# Generated by Django 2.1.5 on 2019-06-23 16:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0017_auto_20190623_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 23, 16, 53, 34, 434736, tzinfo=utc)),
        ),
    ]