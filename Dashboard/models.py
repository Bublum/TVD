from django.db import models


def vehicle_detection_directory(instance, filename):
    return 'Media/Vehicle/{0}/{1}'.format(instance.vehicle_type.vehicle_type, filename)
def vehicle_monitor_directory(instance, filename):
    return 'Media/Vehicle/{0}/{1}'.format(instance.number, filename)


class Model(models.Model):
    model_type = models.CharField(max_length=100)
    model = models.FileField(max_length=1000)
    label = models.FileField(max_length=1000)
    model_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


class VehicleTypeMaster(models.Model):
    vehicle_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


class VehicleMonitor(models.Model):
    number = models.CharField(max_length=15, null=True, blank=True)
    mobile = models.PositiveIntegerField(default='8554951545')
    address = models.CharField(max_length=250, default='test')
    vehicel_type = models.ForeignKey(VehicleTypeMaster, on_delete=models.CASCADE)
    image = models.FileField(max_length=1000, upload_to=vehicle_monitor_directory)
    is_done = models.BooleanField(default=False)


class Camera(models.Model):
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


class Input(models.Model):
    file = models.FileField(max_length=1000)
    name = models.CharField(max_length=200, unique=True)
    file_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_processed = models.BooleanField(default=False)
    location = models.ForeignKey(Camera, on_delete=models.CASCADE)

class ViolationMaster(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    fine_amount = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


# class ViolationDetection(models.Model):
#     detection = models.ForeignKey(Detection, on_delete=models.CASCADE)
#     violation = models.ForeignKey(ViolationMaster, on_delete=models.CASCADE)

class VehicleViolation(models.Model):
    vehicle = models.ForeignKey(VehicleMonitor, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    violation = models.ForeignKey(ViolationMaster, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    has_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class Config(models.Model):
    model = models.FileField(max_length=1000)
    fps = models.DecimalField(max_digits=7, decimal_places=3)
    min_threshold = models.DecimalField(max_digits=7, decimal_places=3)
    max_predict_class = models.PositiveIntegerField()


class VehicleDetection(models.Model):
    image = models.ImageField(upload_to=vehicle_detection_directory)
    vehicle_type = models.ForeignKey(VehicleTypeMaster, on_delete=models.CASCADE)
    location = models.ForeignKey(Camera, on_delete=models.CASCADE)
