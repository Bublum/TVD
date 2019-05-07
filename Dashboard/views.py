from django.shortcuts import render

# Create your views here.
from Dashboard.models import Input, Model, ViolationMaster
import tensorflow as tf
import cv2

from Dashboard.tasks import add, vehicle_detection, number_plate_detection


def homepage(request):
    if request.method == 'GET':
        # vehicle_detection.delay()
        # vehicle_detection.apply_async(queue='vehicle_detection')
        number_plate_detection.apply_async(queue='number_plate_detection')
        # all_input = Input.objects.filter(is_active=True)
        #
        # input_json = {}
        #
        # for each_input in all_input:
        #     input_json[each_input.name] = each_input.model.path

        return render(request, 'html/video_chooser.html')

    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        input = Input.objects.get(id=video_id)
        detection_objs = Model.objects.filter(is_active=True)
        violations = ViolationMaster.objects.filter(is_active=True)
        return render(request, 'html/violation_chooser.html',
                      {'violation_objs': violations, 'detection_objs': detection_objs})


def violation(request):
    return render(request, 'html/violation_chooser.html')
