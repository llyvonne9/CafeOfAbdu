# Generated by Django 2.1.7 on 2019-04-17 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_auto_20190414_2121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='likes',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='num_likes',
            field=models.IntegerField(default=1),
        ),
    ]