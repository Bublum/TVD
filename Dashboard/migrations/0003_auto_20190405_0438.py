# Generated by Django 2.1.1 on 2019-04-05 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0002_auto_20190404_1954'),
    ]

    operations = [
        migrations.RenameField(
            model_name='input',
            old_name='file',
            new_name='model',
        ),
    ]
