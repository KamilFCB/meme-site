# Generated by Django 3.0.1 on 2020-01-05 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memes_site', '0005_auto_20200103_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='memes_site.Image'),
            preserve_default=False,
        ),
    ]
