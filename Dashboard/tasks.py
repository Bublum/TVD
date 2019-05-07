import copy
import math

import cv2
from PIL import Image
from celery import Celery, shared_task

# from Dashboard.models import Input, Detection
import tensorflow as tf
import numpy as np
from django.core.files import File
from django.core.files.images import ImageFile
from django.forms import FileField

from Dashboard.config import maximum_classes_to_detect, min_score_thresh, categories_to_detect, dps
from Dashboard.models import Model, Input, VehicleTypeMaster, VehicleDetection, NumberPlateDetection
from object_detection.functions import count_frames_manual, load_image_into_numpy_array
from object_detection.ops import reframe_box_masks_to_image_masks
from object_detection.utils import label_map_util

app = Celery('tasks', backend='rpc://', broker='amqp://test:test@127.0.0.1//')


@shared_task
def add(x, y):
    for i in range(1, 500000):
        print(i)
    return x + y


def load_graph(model_path):
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        # print(os.path.exists(model['path']))
        with tf.gfile.GFile(model_path, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    return detection_graph


@app.task
def vehicle_detection(id):
    detection_obj = Model.objects.get(model_type='Vehicle', is_active=True)

    model_path = detection_obj.model.path
    input_obj = Input.objects.get(pk=int(id))
    model_label = detection_obj.label.path

    detection_graph = load_graph(model_path)

    # for input_obj in all_input:
    input_path = input_obj.file.path
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
    # total_frames = count_frames_manual(cap)
    print('Total frames', length)
    with detection_graph.as_default():
        with tf.Session() as sess:
            for each_frame in range(math.ceil(length / dps)):
                print(each_frame)
                rev, image_np = cap.read()
                # img.save('my.png')
                # img.show()
                # cv2.imshow('test', image_np)

                # the array based representation of the image will be used later in order to prepare the
                # result image with boxes and labels on it.
                # Expand dimensions since the Prediction expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image_np, axis=0)
                # Actual detection.
                ops = tf.get_default_graph().get_operations()
                all_tensor_names = {output.name for op in ops for output in op.outputs}
                tensor_dict = {}
                for key in [
                    'num_detections', 'detection_boxes', 'detection_scores',
                    'detection_classes', 'detection_masks'
                ]:
                    tensor_name = key + ':0'
                    if tensor_name in all_tensor_names:
                        tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                            tensor_name)
                if 'detection_masks' in tensor_dict:
                    # The following processing is only for single image
                    detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                    detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                    # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                    real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                    detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                    detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                    detection_masks_reframed = reframe_box_masks_to_image_masks(
                        detection_masks, detection_boxes, image_np.shape[0], image_np.shape[1])
                    detection_masks_reframed = tf.cast(
                        tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                    # Follow the convention by adding back the batch dimension
                    tensor_dict['detection_masks'] = tf.expand_dims(
                        detection_masks_reframed, 0)
                image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

                # Run inference
                output_dict = sess.run(tensor_dict,
                                       feed_dict={image_tensor: np.expand_dims(image_np, 0)})

                # all outputs are float32 numpy arrays, so convert types as appropriate
                output_dict['num_detections'] = int(output_dict['num_detections'][0])
                output_dict['detection_classes'] = output_dict[
                    'detection_classes'][0].astype(np.uint8)
                output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
                output_dict['detection_scores'] = output_dict['detection_scores'][0]
                if 'detection_masks' in output_dict:
                    output_dict['detection_masks'] = output_dict['detection_masks'][0]

                image_np_copy = copy.deepcopy(image_np)

                num_detected_vehicles = output_dict['num_detections']
                # print(num_detected_vehicles)
                for i in range(num_detected_vehicles):
                    # print(output_dict)
                    if output_dict['detection_scores'][i] >= min_score_thresh:
                        try:
                            class_name = category_index[output_dict['detection_classes'][i]]['name']
                        except:
                            continue
                        if class_name in categories_to_detect:
                            coord = output_dict['detection_boxes'][i]
                            y1, x1, y2, x2 = coord[0], coord[1], coord[2], coord[3]
                            y1 = int(y1 * image_np.shape[0])
                            y2 = int(y2 * image_np.shape[0])
                            x1 = int(x1 * image_np.shape[1])
                            x2 = int(x2 * image_np.shape[1])
                            # print(x1, x2, y1, y2)
                            cropped_img = image_np[y1:y2, x1:x2]
                            class_obj = VehicleTypeMaster.objects.get(type=class_name)
                            rescaled = np.uint8(cropped_img)
                            im = (Image.fromarray(rescaled, 'RGB'))
                            # cv2.imshow('test', cv2.resize(image_np_copy, (800, 600)))
                            # im.show()
                            img = Image.fromarray(cropped_img, 'RGB')
                            image_name = str(each_frame) + '_' + str(i) + '.png'
                            img.save(image_name)
                            v = VehicleDetection(vehicle_type=class_obj)
                            v.image.save(image_name, File(open(image_name, 'rb')))
                            v.save()
                cap.set(1, each_frame * dps)
        input_obj.is_processed = True
        input_obj.save()
    cap.release()
    return True


@app.task
def number_plate_detection():
    detection_obj = Model.objects.get(model_type='number_plate', is_active=True)
    model_path = detection_obj.model.path
    detection_graph = load_graph(model_path)

    all_input = VehicleDetection.objects.filter(is_processed=False)
    model_label = detection_obj.label.path

    with detection_graph.as_default():
        with tf.Session() as sess:
            for each_input in all_input:
                image_path = each_input.image.path
                # cap = cv2.imread()
                print(image_path)
                image = Image.open(image_path)
                image_np = load_image_into_numpy_array(image)

                label_map = label_map_util.load_labelmap(model_label)
                categories = label_map_util.convert_label_map_to_categories(label_map,
                                                                            max_num_classes=maximum_classes_to_detect,
                                                                            use_display_name=True)
                category_index = label_map_util.create_category_index(categories)
                # total_frames = count_frames_manual(cap)

                # the array based representation of the image will be used later in order to prepare the
                # result image with boxes and labels on it.
                # Expand dimensions since the Prediction expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image_np, axis=0)
                # Actual detection.
                ops = tf.get_default_graph().get_operations()
                all_tensor_names = {output.name for op in ops for output in op.outputs}
                tensor_dict = {}
                for key in [
                    'num_detections', 'detection_boxes', 'detection_scores',
                    'detection_classes', 'detection_masks'
                ]:
                    tensor_name = key + ':0'
                    if tensor_name in all_tensor_names:
                        tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                            tensor_name)
                if 'detection_masks' in tensor_dict:
                    # The following processing is only for single image
                    detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                    detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                    # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                    real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                    detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                    detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                    detection_masks_reframed = reframe_box_masks_to_image_masks(
                        detection_masks, detection_boxes, image_np.shape[0], image_np.shape[1])
                    detection_masks_reframed = tf.cast(
                        tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                    # Follow the convention by adding back the batch dimension
                    tensor_dict['detection_masks'] = tf.expand_dims(
                        detection_masks_reframed, 0)
                image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

                # Run inference
                output_dict = sess.run(tensor_dict,
                                       feed_dict={image_tensor: np.expand_dims(image_np, 0)})

                # all outputs are float32 numpy arrays, so convert types as appropriate
                output_dict['num_detections'] = int(output_dict['num_detections'][0])
                output_dict['detection_classes'] = output_dict[
                    'detection_classes'][0].astype(np.uint8)
                output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
                output_dict['detection_scores'] = output_dict['detection_scores'][0]
                if 'detection_masks' in output_dict:
                    output_dict['detection_masks'] = output_dict['detection_masks'][0]

                image_np_copy = copy.deepcopy(image_np)

                num_detected_vehicles = output_dict['num_detections']
                # print(num_detected_vehicles)
                for i in range(num_detected_vehicles):
                    # print(output_dict)
                    if output_dict['detection_scores'][i] >= min_score_thresh:
                        try:
                            class_name = category_index[output_dict['detection_classes'][i]]['name']
                        except:
                            continue
                        if class_name in categories_to_detect:
                            coord = output_dict['detection_boxes'][i]
                            y1, x1, y2, x2 = coord[0], coord[1], coord[2], coord[3]
                            y1 = int(y1 * image_np.shape[0])
                            y2 = int(y2 * image_np.shape[0])
                            x1 = int(x1 * image_np.shape[1])
                            x2 = int(x2 * image_np.shape[1])
                            print(x1, x2, y1, y2)
                            cropped_img = image_np[y1:y2, x1:x2]
                            class_obj = VehicleTypeMaster.objects.get(vehicle_type=class_name)
                            rescaled = np.uint8(cropped_img)
                            # im = (Image.fromarray(rescaled, 'RGB'))
                            # cv2.imshow('test', cv2.resize(image_np_copy, (800, 600)))
                            # im.show()
                            img = Image.fromarray(cropped_img, 'RGB')
                            img.save('my.png')
                            v = NumberPlateDetection(vehicle_detection=each_input)
                            v.image.save('aaaa', File(open('my.png', 'rb')))
                            v.save()
    return True
