# Generated by Django 3.1.5 on 2021-04-12 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follower',
            name='follow',
        ),
    ]