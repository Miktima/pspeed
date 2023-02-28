# Generated by Django 4.1.6 on 2023-02-28 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getdata', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data',
            old_name='data',
            new_name='dataLEDesktop',
        ),
        migrations.AddField(
            model_name='data',
            name='dataLEMobile',
            field=models.JSONField(default=dict),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='dataOLEDesktop',
            field=models.JSONField(default=dict),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='dataOLEMobile',
            field=models.JSONField(default=dict),
            preserve_default=False,
        ),
    ]