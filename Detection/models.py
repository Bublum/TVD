from django.db import models


# Create your models here.


class VehicleDetection(models.Model):
    number = models.CharField(max_length=15, null=True, blank=True)
    mobile = models.PositiveIntegerField(default='8554951545')
    address = models.CharField(max_length=250, default='test')
    type = models.CharField(max_length=100)
    image_path = models.CharField(max_length=500)
    is_done = models.BooleanField(default=False)


class Camera(models.Model):
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


class Input(models.Model):
    path = models.CharField(max_length=1000)
    name = models.CharField(max_length=200, unique=True)
    file_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)


class Violation(models.Model):
    description = models.CharField(max_length=200)
    fine_amount = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


class VehicleViolation(models.Model):
    vehicle = models.ForeignKey(VehicleDetection, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    violation = models.ForeignKey(Violation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    has_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

# class Config(models.Model):
