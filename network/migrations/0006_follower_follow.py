# Generated by Django 3.1.5 on 2021-04-12 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_remove_follower_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='follower',
            name='follow',
            field=models.BooleanField(default=False),
        ),
    ]