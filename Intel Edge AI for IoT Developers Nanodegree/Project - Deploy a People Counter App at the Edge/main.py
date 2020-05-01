"""People Counter."""
"""
 Copyright (c) 2018 Intel Corporation.
 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit person to whom the Software is furnished to do so, subject to
 the following conditions:
 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import os
import sys
import time
import socket
import json
import cv2
from collections import deque

import numpy as np
import tensorflow as tf
import cv2 as cv

import logging as log
import paho.mqtt.client as mqtt

from argparse import ArgumentParser
from inference import Network

# log
handler = log.FileHandler('{}.log'.format(__name__))
logger = log.getLogger(__name__)
logger.setLevel(log.DEBUG)
logger.addHandler(handler)

# MQTT server environment variables
HOSTNAME = socket.gethostname()
IPADDRESS = socket.gethostbyname(HOSTNAME)
MQTT_HOST = IPADDRESS
MQTT_PORT = 3001
MQTT_KEEPALIVE_INTERVAL = 60

CPU_EXTENSION = "/opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so"
MODEL = "/home/workspace/ssd_inception_v2_coco_2018_01_28/frozen_inference_graph.xml"

def build_argparser():
    """
    Parse command line arguments.

    :return: command line arguments
    """
    parser = ArgumentParser()
    parser.add_argument("-m", "--model", required=False,default=MODEL, type=str,
                        help="Path to an xml file with a trained model.")
    parser.add_argument("-i", "--input", required=True, type=str,
                        help="Path to image or video file")
    parser.add_argument("-l", "--cpu_extension", required=False, type=str,
                        default=None,
                        help="MKLDNN (CPU)-targeted custom layers."
                             "Absolute path to a shared library with the"
                             "kernels impl.")
    parser.add_argument("-d", "--device", type=str, default="CPU",
                        help="Specify the target device to infer on: "
                             "CPU, GPU, FPGA or MYRIAD is acceptable. Sample "
                             "will look for a suitable plugin for device "
                             "specified (CPU by default)")
    parser.add_argument("-pt", "--prob_threshold", type=float, default=0.5,
                        help="Probability threshold for detections filtering"
                        "(0.5 by default)")
    return parser


def connect_mqtt():
    ### TODO: Connect to the MQTT client ###
    client = mqtt.Client()
    client.connect(MQTT_HOST,MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

    return client

acc_total = 0
acc_count = 0
def draw_boxes(frame, results, prop, width, height):
    global acc_total, acc_count
    num_person = 0
    for box in results[0][0]:
        bclass = box[1] # 1 person
        if bclass != 1:
            continue
        conf = box[2]
        acc_count += 1
        acc_total += conf
        logger.debug("acc = {}".format(acc_total / acc_count))
        if(conf > prop):
            num_person += 1
            xmin = int(box[3] * width)
            ymin = int(box[4] * height)
            xmax = int(box[5] * width)
            ymax = int(box[6] * height)
            cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), 1, 3)
    return frame, num_person

def infer_on_stream(args, client):
    """
    Initialize the inference network, stream video to network,
    and output stats and video.

    :param args: Command line arguments parsed by `build_argparser()`
    :param client: MQTT client
    :return: None
    """
    # Initialise the class
    infer_network = Network()
    # Set Probability threshold for detections
    prob_threshold = args.prob_threshold

    ### TODO: Load the model through `infer_network` ###
    infer_network.load_model(args.model, args.device, args.cpu_extension)
    ### TODO: Handle the input stream ###
    
    if args.input =='CAM':
        input_stream = 0
        single_image = False
    elif args.input[-4:] in [".jpg", ".bmp"]:
        single_image = True
        input_stream = args.input
    else:
        single_image=False
        input_stream = args.input
        assert os.path.isfile(input_stream)
        
    stream = cv2.VideoCapture(args.input)
    stream.open(args.input)
    
    if not stream.isOpened():
        logger.error("Unable to open video.")
        
    width = int(stream.get(3))
    height = int(stream.get(4))
    
    ### TODO: Loop until stream is over ###
    last_count = 0
    total_count = 0
    
    maxlen = 24
    request_id = 0
    passed_counts = deque(maxlen = maxlen)
    while stream.isOpened():
        ### TODO: Read from the video capture ###
        flag, frame = stream.read()
        if not flag:
            break
        ### TODO: Pre-process the image as needed ###
        ishape = infer_network.get_input_shape()
#         logger.debug("shape: {}".format(ishape) )
        p_frame = cv2.resize(frame, (ishape[3], ishape[2]))
        p_frame = p_frame.transpose((2,0,1))
        p_frame = p_frame.reshape(1, *p_frame.shape)
        
        t0 = time.time()
        ### TODO: Start asynchronous inference for specified request ###
        infer_network.exec_net(request_id, p_frame)
        ### TODO: Wait for the result ###
        if infer_network.wait(request_id) == 0:
            ### TODO: Get the results of the inference request ###
            result = infer_network.get_output(request_id) # 'DetectionOutput'
            logger.debug("process_time = {}".format(time.time() - t0))
#             logger.debug(result)
            ### TODO: Extract any desired stats from the results ###
            out_frame, temp_count = draw_boxes(frame, result, prob_threshold, width, height)
            
            
            passed_counts.append(temp_count)
            current_count = 0
            if sum(passed_counts) / maxlen > 0.2:
                current_count = 1
                
            ### TODO: Calculate and send relevant information on ###
            ### current_count, total_count and duration to the MQTT server ###
            ### Topic "person": keys of "count" and "total" ###
            ### Topic "person/duration": key of "duration" ###
            if current_count > last_count:
                start_time = time.time()
                total_count = total_count + current_count - last_count
                last_count = current_count
                client.publish("person", json.dumps({"total": total_count}), retain=True)
            if current_count < last_count:
                duration = int(time.time() - start_time)
                client.publish("person/duration",
                               json.dumps({"duration": duration}), retain=True)
                last_count = current_count
            client.publish("person", json.dumps({"count": current_count}), retain=True)
            
        ### TODO: Send the frame to the FFMPEG server ###
        sys.stdout.buffer.write(out_frame)
        sys.stdout.flush()
        
        ### TODO: Write an output image if `single_image_mode` ###
        if single_image:
            cv2.imwrite("output.jpg", bb_frame)
            
    stream.release()
    cv2.destroyAllWindows()
    client.disconnect()
    
def main():
    """
    Load the network and parse the output.

    :return: None
    """
    # Grab command line args
    args = build_argparser().parse_args()
    
    # Connect to the MQTT server
    client = connect_mqtt()
    # Perform inference on the input stream
    infer_on_stream(args, client)


if __name__ == '__main__':
    main()
