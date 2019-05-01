from celery import Celery

from Dashboard.models import Input
import tensorflow as tf

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def add(x, y):
    return x + y


@app.task
def vehicle_detection(x, y):
    # Load graph
    detection_graph = tf.Graph()

    detection_obj = Detection.objects.get(pk=detection_id)
    all_input = Input.objects.filter(is_processed=False)

    for each in all_input:

        model_path = input_obj.model.path
    return x + y
