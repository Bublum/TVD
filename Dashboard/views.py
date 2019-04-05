from django.shortcuts import render

# Create your views here.
from Dashboard.models import Input, Detection, ViolationMaster
import tensorflow as tf
import cv2


def homepage(request):
    if request.method == 'GET':
        all_input = Input.objects.filter(is_active=True)

        # input_json = {}
        #
        # for each_input in all_input:
        #     input_json[each_input.name] = each_input.file.path

        return render(request, 'html/video_chooser.html', {'all_input': all_input})

    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        input = Input.objects.get(id=video_id)
        detection_objs = Detection.objects.filter(is_active=True)
        violations = ViolationMaster.objects.filter(is_active=True)
        return render(request, 'html/violation_chooser.html', {'violation_objs': violations, 'detection_objs':detection_objs})


def violation(request):

    return render(request, 'html/violation_chooser.html')

def start_prediction(request):
    # Load graph
    detection_graph = tf.Graph()

    detection_id = int(request.session.get('detection_id'))
    input_id = int(request.session.get('video_id'))

    detection_obj = Detection.objects.get(pk=detection_id)
    input_obj = Input.objects.get(pk=input_id)

    model_path = input_obj.model.path

    cap = cv2.VideoCapture(input_obj.model.path)

    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
