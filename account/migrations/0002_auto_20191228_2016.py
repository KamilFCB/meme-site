# Generated by Django 3.0.1 on 2019-12-28 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email_text',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='password_text',
            new_name='password',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='username_text',
            new_name='username',
        ),
    ]
