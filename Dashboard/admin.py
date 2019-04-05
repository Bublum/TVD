from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(VehicleDetection)
admin.site.register(Detection)
admin.site.register(Input)
admin.site.register(ViolationMaster)
admin.site.register(Camera)
admin.site.register(VehicleViolation)
admin.site.register(Config)