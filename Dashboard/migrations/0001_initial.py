# Generated by Django 2.1.1 on 2019-05-09 19:47

import Dashboard.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CameraMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('serial_number', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.FileField(max_length=1000, upload_to='')),
                ('fps', models.DecimalField(decimal_places=3, max_digits=7)),
                ('min_threshold', models.DecimalField(decimal_places=3, max_digits=7)),
                ('max_predict_class', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Input',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=1000, upload_to=Dashboard.models.input_video_directory)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('file_type', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('is_processed', models.BooleanField(default=False)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashboard.CameraMaster')),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_type', models.CharField(max_length=100)),
                ('model', models.FileField(max_length=1000, upload_to=Dashboard.models.model_directory)),
                ('label', models.FileField(max_length=1000, upload_to=Dashboard.models.label_directory)),
                ('model_name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='NumberPlate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='NumberPlateDetection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(max_length=1000, upload_to=Dashboard.models.number_plate_directory)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleDetection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(max_length=1000, upload_to=Dashboard.models.vehicle_detection_directory)),
                ('is_processed', models.BooleanField(default=False)),
                ('original_frame', models.CharField(default='', max_length=5000)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashboard.CameraMaster')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleMonitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.PositiveIntegerField(default='8554951545')),
                ('timestamp', models.DateTimeField()),
                ('image', models.FileField(max_length=1000, upload_to=Dashboard.models.vehicle_monitor_directory)),
                ('number_detection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashboard.NumberPlateDetection')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleTypeMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=15)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleViolation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_paid', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_processed', models.BooleanField(default=False)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashboard.CameraMaster')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashboard.VehicleMonitor')),
            ],
        ),
        migrations.CreateModel(
            name='ViolationMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('fine_amount', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='vehicleviolation',
            name='violation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashboard.ViolationMaster'),
        ),
        migrations.AddField(
            model_name='vehicledetection',
            name='vehicle_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashboard.VehicleTypeMaster'),
        ),
        migrations.AddField(
            model_name='numberplatedetection',
            name='vehicle_detection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashboard.VehicleDetection'),
        ),
    ]
