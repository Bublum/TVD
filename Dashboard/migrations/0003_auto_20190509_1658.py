# Generated by Django 2.0.6 on 2019-05-09 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0002_auto_20190509_1657'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicledetection',
            old_name='original_path',
            new_name='original_frame',
        ),
    ]
