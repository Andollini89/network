# Generated by Django 3.1.5 on 2021-04-07 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_remove_newpost_likes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewPost',
            new_name='Post',
        ),
    ]
