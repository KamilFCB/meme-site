# Generated by Django 3.0.1 on 2020-01-01 20:07

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('memes_site', '0003_auto_20200101_1758'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Post',
            new_name='Image',
        ),
    ]