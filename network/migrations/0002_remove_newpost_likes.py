# Generated by Django 3.1.5 on 2021-04-02 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newpost',
            name='likes',
        ),
    ]
