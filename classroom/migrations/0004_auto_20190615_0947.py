# Generated by Django 2.1.5 on 2019-06-15 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0003_auto_20190615_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.Subject'),
        ),
    ]
