# Generated by Django 2.1.1 on 2019-05-07 10:21

import Dashboard.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('Dashboard', '0010_auto_20190501_1818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehiclemonitor',
            name='vehicel_type',
        ),
        migrations.AddField(
            model_name='vehicledetection',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vehiclemonitor',
            name='vehicle_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE,
                                    to='Dashboard.VehicleTypeMaster'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='input',
            name='file',
            field=models.FileField(max_length=1000, upload_to=Dashboard.models.input_video_directory),
        ),
    ]