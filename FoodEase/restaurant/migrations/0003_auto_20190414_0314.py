# Generated by Django 2.1.1 on 2019-04-14 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_auto_20190414_0238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='lng',
        ),
    ]
