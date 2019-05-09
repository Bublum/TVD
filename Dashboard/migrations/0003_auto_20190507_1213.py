# Generated by Django 2.1.1 on 2019-05-07 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('Dashboard', '0002_auto_20190507_1155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicledetection',
            name='type',
        ),
        migrations.RemoveField(
            model_name='vehiclemonitor',
            name='address',
        ),
        migrations.RemoveField(
            model_name='vehiclemonitor',
            name='number',
        ),
        migrations.RemoveField(
            model_name='vehiclemonitor',
            name='vehicle_type',
        ),
        migrations.AddField(
            model_name='vehicledetection',
            name='vehicle_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE,
                                    to='Dashboard.VehicleTypeMaster'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehiclemonitor',
            name='number_detection',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE,
                                    to='Dashboard.NumberPlateDetection'),
            preserve_default=False,
        ),
    ]
