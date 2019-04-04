# Generated by Django 2.1.1 on 2019-04-04 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
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
            name='Detection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_type', models.CharField(max_length=100)),
                ('model_path', models.FileField(max_length=1000, upload_to='')),
                ('model_name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Input',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=1000, upload_to='')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('file_type', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleDetection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=15, null=True)),
                ('mobile', models.PositiveIntegerField(default='8554951545')),
                ('address', models.CharField(default='test', max_length=250)),
                ('type', models.CharField(max_length=100)),
                ('image', models.FileField(max_length=1000, upload_to='')),
                ('is_done', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleViolation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('has_paid', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashboard.Camera')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashboard.VehicleDetection')),
            ],
        ),
        migrations.CreateModel(
            name='ViolationMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('fine_amount', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='vehicleviolation',
            name='violation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashboard.ViolationMaster'),
        ),
    ]
