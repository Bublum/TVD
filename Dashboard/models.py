from django.db import models



def vehicle_detection_directory(instance, filename):
    return 'Vehicle/{0}/{1}.png'.format(instance.vehicle_type.type, filename)


def vehicle_monitor_directory(instance, filename):
    return 'Vehicle/{0}/{1}'.format(instance.number_detection.number_plate, filename)


def model_directory(instance, filename):
    return 'Model/{0}/{1}'.format(instance.model_type, filename)


def label_directory(instance, filename):
    return 'Label/{0}/{1}'.format(instance.model_type, filename)


def input_video_directory(instance, filename):
    return 'Input/{0}'.format(filename)


def number_plate_directory(instance, filename):
    return 'Number_Plate/{0}'.format(filename)


class Model(models.Model):
    model_type = models.CharField(max_length=100)
    model = models.FileField(max_length=1000, upload_to=model_directory)
    label = models.FileField(max_length=1000, upload_to=label_directory)
    model_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


class CameraMaster(models.Model):
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.serial_number + ' - ' + self.location


class VehicleTypeMaster(models.Model):
    type = models.CharField(max_length=15)
    # number = models.CharField(max_length=15, null=True, blank=True)
    # mobile = models.PositiveIntegerField(default='8554951545')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.type


class VehicleDetection(models.Model):
    # vehicle = models.ForeignKey(VehicleMaster, on_delete=models.CASCADE)
    # address = models.CharField(max_length=250, default='test')
    vehicle_type = models.ForeignKey(VehicleTypeMaster, on_delete=models.CASCADE)
    camera = models.ForeignKey(CameraMaster, on_delete=models.CASCADE)
    image = models.FileField(upload_to=vehicle_detection_directory, max_length=1000)
    is_processed = models.BooleanField(default=False)
    original_frame = models.CharField(max_length=5000, default='')

    def __str__(self):
        return str(type) + str(self.camera)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.save()
        from Dashboard.tasks import number_plate_detection
        monitor_obj_id = number_plate_detection(self.pk)
        if self.vehicle_type.type == 'motorcycle':
            from Dashboard.tasks import helmet_detection
            helmet_detection(self.pk, monitor_obj_id)


class NumberPlate(models.Model):
    number = models.CharField(max_length=15)

    def __str__(self):
        return self.number


class NumberPlateDetection(models.Model):
    # number_plate = models.ForeignKey(NumberPlate, on_delete=models.CASCADE)
    image = models.FileField(upload_to=number_plate_directory, max_length=1000)
    vehicle_detection = models.ForeignKey(VehicleDetection, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.number_plate


class Input(models.Model):
    file = models.FileField(max_length=1000, upload_to=input_video_directory)
    name = models.CharField(max_length=200, unique=True)
    file_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_processed = models.BooleanField(default=False)
    camera = models.ForeignKey(CameraMaster, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.save()
        from Dashboard.tasks import vehicle_detection
        vehicle_detection.apply_async(args=[str(self.pk)], queue='vehicle_detection')


class VehicleMonitor(models.Model):
    number_detection = models.ForeignKey(NumberPlateDetection, on_delete=models.CASCADE)
    mobile = models.PositiveIntegerField(default='8554951545')
    timestamp = models.DateTimeField()
    # address = models.CharField(max_length=250, default='test')
    # vehicle_type = models.ForeignKey(VehicleTypeMaster, on_delete=models.CASCADE)
    image = models.FileField(max_length=1000, upload_to=vehicle_monitor_directory)

    # is_done = models.BooleanField(default=False)

    def __str__(self):
        return str(self.number_detection)


# class ViolationDetection(models.Model):
#     detection = models.ForeignKey(Detection, on_delete=models.CASCADE)
#     violation = models.ForeignKey(ViolationMaster, on_delete=models.CASCADE)

class ViolationMaster(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    fine_amount = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class VehicleViolation(models.Model):
    vehicle = models.ForeignKey(VehicleMonitor, on_delete=models.CASCADE)
    camera = models.ForeignKey(CameraMaster, on_delete=models.CASCADE)
    violation = models.ForeignKey(ViolationMaster, on_delete=models.CASCADE)
    has_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.vehicle) + ' - ' + str(self.violation)


class Config(models.Model):
    model = models.FileField(max_length=1000)
    fps = models.DecimalField(max_digits=7, decimal_places=3)
    min_threshold = models.DecimalField(max_digits=7, decimal_places=3)
    max_predict_class = models.PositiveIntegerField()
