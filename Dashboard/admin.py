from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(VehicleDetection)
admin.site.register(NumberPlateDetection)
admin.site.register(Model)
admin.site.register(Input)
admin.site.register(ViolationMaster)
admin.site.register(CameraMaster)
admin.site.register(VehicleViolation)
admin.site.register(Config)
admin.site.register(VehicleTypeMaster)
admin.site.register(VehicleMonitor)
admin.site.register(NumberPlate)
