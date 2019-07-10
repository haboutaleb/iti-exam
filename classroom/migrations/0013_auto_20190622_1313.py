# Generated by Django 2.1.5 on 2019-06-22 13:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0012_auto_20190622_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 22, 13, 13, 38, 811880, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='subject',
            name='chapter_num',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='subject',
            name='question_num_ramining',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='subject',
            name='question_num_understanding',
            field=models.IntegerField(default=1),
        ),
    ]
