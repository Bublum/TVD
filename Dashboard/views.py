import datetime

from django.shortcuts import render

# Create your views here.
from Dashboard.models import Input, Model, ViolationMaster, VehicleViolation
import tensorflow as tf
import cv2

from Dashboard.tasks import add, vehicle_detection


def homepage(request):
    if request.method == 'GET':
        # vehicle_detection.delay()
        all_input = Input.objects.filter(is_processed=False)
        for each_input in all_input:
            vehicle_detection.apply_async(args=[str(each_input.pk)], queue='feed_tasks')

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


def daywise(request):
    if request.method == 'GET':
        return render(request, 'html/daywise.html')
    else:
        selected_date = datetime.datetime.strptime(request.POST.get('selected_date'), '%d-%m-%Y').date()
        start_timestamp = datetime.datetime.combine(selected_date, datetime.time.min)
        end_timestamp = datetime.datetime.combine(selected_date, datetime.time.max)
        violations = VehicleViolation.objects.filter(timestamp__range=(start_timestamp, end_timestamp))
        if len(violations) == 0:
            message = 'No violations on selected date.'
            return render(request, 'html/daywise.html', {
                'selected_date': selected_date,
                'message': message
            })

        else:
            return render(request, 'html/daywise.html', {
                'selected_date': selected_date,
                'violations': violations
            })
