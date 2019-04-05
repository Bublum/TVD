from django.db import models


# Create your models here.

class Detection(models.Model):
    model_type = models.CharField(max_length=100)
    model_path = models.FileField(max_length=1000)
    model_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


class VehicleDetection(models.Model):
    number = models.CharField(max_length=15, null=True, blank=True)
    mobile = models.PositiveIntegerField(default='8554951545')
    address = models.CharField(max_length=250, default='test')
    type = models.CharField(max_length=100)
    image = models.FileField(max_length=1000)
    is_done = models.BooleanField(default=False)


class Camera(models.Model):
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


class Input(models.Model):
    model = models.FileField(max_length=1000)
    name = models.CharField(max_length=200, unique=True)
    file_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)


class ViolationMaster(models.Model):
    description = models.CharField(max_length=200)
    fine_amount = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)




class VehicleViolation(models.Model):
    vehicle = models.ForeignKey(VehicleDetection, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    violation = models.ForeignKey(ViolationMaster, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    has_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class Config(models.Model):
    model = models.FileField(max_length=1000)
    fps = models.DecimalField()
    min_threshold = models.DecimalField()
    max_predict_class = models.PositiveIntegerField()
