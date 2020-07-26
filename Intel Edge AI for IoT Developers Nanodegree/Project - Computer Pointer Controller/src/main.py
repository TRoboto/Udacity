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

import numpy as np

import logging as log

from argparse import ArgumentParser

from input_feeder import InputFeeder
from face_detection import Model_Face_Detection
from facial_landmarks_detection import Model_Facial_Landmarks_Detection
from gaze_estimation import Model_Gaze_Estimation
from head_pose_estimation import Model_Head_Pose_Estimation
from mouse_controller import MouseController

# log
handler = log.FileHandler('{}.log'.format(__name__))
logger = log.getLogger(__name__)
logger.setLevel(log.DEBUG)
logger.addHandler(handler)


CPU_EXTENSION = "/opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so"

def build_argparser():
    """
    Parse command line arguments.

    :return: command line arguments
    """
    parser = ArgumentParser()
    parser.add_argument("-f", "--facedetectionmodel", required=True, type=str,
                        help=" Path to .xml file of the Face Detection model.")
    parser.add_argument("-fl", "--faciallandmarkmodel", required=True, type=str,
                        help=" Path to .xml file of the Facial Landmark Detection model.")
    parser.add_argument("-hp", "--headposemodel", required=True, type=str,
                        help=" Path to .xml file of the Head Pose Estimation model.")
    parser.add_argument("-g", "--gazeestimationmodel", required=True, type=str,
                        help=" Path to .xml file of the Gaze Estimation model.")
    parser.add_argument("-i", "--input", required=True, type=str,
                        help="Path to image or video file")
    parser.add_argument("-flags", "--flags", required=False, nargs='+',
                        default=[],
                        help="Specify the flags like --flags fd hp fld ge"
                             "if you want to visualize different models output at each frame," 
                             "fd for Face Detection, fld for Facial Landmark Detection"
                             "hp for Head Pose Estimation, ge for Gaze Estimation." )
    parser.add_argument("-l", "--cpu_extension", required=False, type=str,
                        default=CPU_EXTENSION,
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

def infer(args):
    """
    Initialize the inference network, and output stats and video.

    :param args: Command line arguments parsed by `build_argparser()`
    :return: None
    """
    # Set Probability threshold for detections
    prob_threshold = args.prob_threshold
    
    if args.input.lower() == "cam":
        input_feeder = InputFeeder("cam")
    else:
        if not os.path.isfile(args.input):
            logger.error("Unable to find input file")
            exit(1)
        
        input_feeder = InputFeeder("video",args.input)

    start_time = time.time()
    model_fd = Model_Face_Detection(args.facedetectionmodel, args.device, args.cpu_extension)
    model_fld = Model_Facial_Landmarks_Detection(args.faciallandmarkmodel, args.device, args.cpu_extension)
    model_ge = Model_Gaze_Estimation(args.gazeestimationmodel, args.device, args.cpu_extension)
    model_hp = Model_Head_Pose_Estimation(args.headposemodel, args.device, args.cpu_extension)
    
    mc = MouseController('medium','fast')

    input_feeder.load_data()

    model_fd.load_model()
    model_fld.load_model()
    model_ge.load_model()
    model_hp.load_model()
    
    loading_time = time.time() - start_time
    logger.info("Loading time of the models: " + str(loading_time) + " s")
    
    frame_count = 0
    inference_time = 0
    for flag, frame in input_feeder.next_batch():
        if not flag:
            break
        if frame is None:
            continue
        key = cv2.waitKey(60)
        if key == 27:
            break
        frame_count += 1
        
        start_inference = time.time()
        face, face_coords = model_fd.predict(frame, prob_threshold)
        if type(face) == int:
            logger.error("No face detected.")
            continue
            
        out_hp = model_hp.predict(face)
        left_eye, right_eye, eye_coords = model_fld.predict(face)
        mouse_coord, gaze_vector = model_ge.predict(left_eye, right_eye, out_hp)
        
        inference_time += time.time() - start_inference
        if len(args.flags) != 0:
            frame_p = frame.copy()
            if 'fd' in args.flags:
                frame_p = face
                
            if 'fld' in args.flags:
                cv2.rectangle(face, (eye_coords[0][0]-10, eye_coords[0][1]-10), (eye_coords[0][2]+10, eye_coords[0][3]+10), (0,255,0), 3)
                cv2.rectangle(face, (eye_coords[1][0]-10, eye_coords[1][1]-10), (eye_coords[1][2]+10, eye_coords[1][3]+10), (0,255,0), 3)
                
            if 'hp' in args.flags:
                cv2.putText(frame_p, "Pose Angles: yaw:{:.2f} | pitch:{:.2f} | roll:{:.2f}".format(out_hp[0],out_hp[1],out_hp[2]), (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.2, (255, 255, 255), 1)
            if 'ge' in args.flags:
                x, y, w = int(gaze_vector[0]*12), int(gaze_vector[1]*12), 160
                le =cv2.line(left_eye, (x-w, y-w), (x+w, y+w), (255,0,255), 2)
                cv2.line(le, (x-w, y+w), (x+w, y-w), (255,0,255), 2)
                re = cv2.line(right_eye, (x-w, y-w), (x+w, y+w), (255,0,255), 2)
                cv2.line(re, (x-w, y+w), (x+w, y-w), (255,0,255), 2)
                face[eye_coords[0][1]:eye_coords[0][3],eye_coords[0][0]:eye_coords[0][2]] = le
                face[eye_coords[1][1]:eye_coords[1][3],eye_coords[1][0]:eye_coords[1][2]] = re
                
            cv2.imshow("visualization",cv2.resize(preview_frame,(500,500)))
			
        inference_time += time.time() - start_inference
        
        # mouse move at 5 FPS
        if frame_count%5 == 0:
            mc.move(mouse_coord[0], new_mouse_coord[1])
        
    
    logger.info("Total inference time {} s".format(inference_time))
    logger.info("Average inference time {} s".format(inference_time/frame_count))
    logger.info("FPS {} frame/second".format(frame_count / (inference_time * 5)))
                 
    cv2.destroyAllWindows()
    input_feeder.close()
    
def main():
    """
    Load the network and parse the output.

    :return: None
    """
    # Grab command line args
    args = build_argparser().parse_args()
    
    # Perform inference on the input
    infer(args)


if __name__ == '__main__':
    main()
