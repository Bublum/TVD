import datetime
import json

from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from Dashboard.models import Input, Model, ViolationMaster, VehicleViolation, VehicleMonitor
import tensorflow as tf
import cv2

from Dashboard.tasks import vehicle_detection, number_plate_detection


def homepage(request):
    if request.method == 'GET':
        # vehicle_detection()
        all_input = Input.objects.filter(is_processed=False)
        for each_input in all_input:
            # vehicle_detection.apply_async(args=[str(each_input.pk)], queue='feed_tasks')
            vehicle_detection(str(each_input.pk))
            # vehicle_detection(each_input.pk)
        # vehicle_detection.apply_async(queue='vehicle_detection')
        # number_plate_detection.apply_async(queue='number_plate_detection')
        # number_plate_detection()
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
        return render(request, 'html/daywise_violation.html')
    else:
        selected_date = datetime.datetime.strptime(request.POST.get('selected_date'), '%d-%m-%Y').date()
        start_timestamp = datetime.datetime.combine(selected_date, datetime.time.min)
        end_timestamp = datetime.datetime.combine(selected_date, datetime.time.max)
        violations = VehicleViolation.objects.filter(timestamp__range=(start_timestamp, end_timestamp))
        if len(violations) == 0:
            message = 'No violations on selected date.'
            return render(request, 'html/daywise_violation.html', {
                'selected_date': selected_date,
                'message': message
            })

        else:
            return render(request, 'html/daywise_violation.html', {
                'selected_date': selected_date,
                'violations': violations
            })


@csrf_exempt
def monitoring(request):
    if request.method == 'GET':
        return render(request, 'html/vehicle_monitoring.html')
    elif request.method == 'POST':
        if request.is_ajax():
            selected_date = datetime.datetime.strptime(request.POST.get('selected_date'), '%m/%d/%Y').date()
            vehicle_number = request.POST.get('vehicle_number')
            start_timestamp = datetime.datetime.combine(selected_date, datetime.time.min)
            end_timestamp = datetime.datetime.combine(selected_date, datetime.time.max)
            results = VehicleMonitor.objects.filter(timestamp__range=(start_timestamp, end_timestamp),
                                                    number_detection__number_plate__number__contains=vehicle_number)

            result_serialized = serializers.serialize('json', results)
            return HttpResponse(result_serialized)
