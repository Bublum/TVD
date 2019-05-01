import cv2
from celery import Celery, shared_task

# from Dashboard.models import Input, Detection
import tensorflow as tf

from object_detection.util import label_map_util

app = Celery('tasks', backend='rpc://', broker='amqp://test:test@127.0.0.1//')


@shared_task
def add(x, y):
    for i in range(1, 500000):
        print(i)
    return x + y


@app.task
def vehicle_detection(x, y):
    # Load graph
    detection_graph = tf.Graph()

    detection_obj = Detection.objects.get(model_name='Vehicle')
    model_path = detection_obj.model_path
    all_input = Input.objects.filter(is_processed=False)
    model_label = detection_obj.label_path

    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        # print(os.path.exists(model['path']))
        with tf.gfile.GFile(model_path, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    for each_input in all_input:
        input_path = each_input.file.path
        cap = cv2.VideoCapture(input_path)

        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        label_map = label_map_util.load_labelmap(model_label)

        categories = label_map_util.convert_label_map_to_categories(label_map,
                                                                    max_num_classes=maximum_classes_to_detect,
                                                                    use_display_name=True)
        category_index = label_map_util.create_category_index(categories)

    return x + y
