# Generated by Django 4.1.6 on 2023-03-01 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getdata', '0002_rename_data_data_dataledesktop_data_datalemobile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
