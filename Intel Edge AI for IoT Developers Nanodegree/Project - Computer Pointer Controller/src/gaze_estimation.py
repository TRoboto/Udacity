'''
This is a sample class for a model. You may choose to use it as-is or make any changes to it.
This has been provided just to give you an idea of how to structure your model class.
'''
import math
import os
import cv2
import numpy as np
from openvino.inference_engine import IENetwork, IECore

class Model_Gaze_Estimation:
    '''
    Class for the Gaze Estimation Model.
    '''
    def __init__(self, model_name, device='CPU', extensions=None):
        '''
        TODO: Use this to set your instance variables.
        '''
        self.model_name = model_name
        self.device = device
        self.extensions = extensions
        self.plugin = None
        self.network = None
        self.input_blob = None
        self.output_blob = None
        self.exec_network = None
        self.infer_request = None

    def load_model(self):
        '''
        TODO: You will need to complete this method.
        This method is for loading the model to the device specified by the user.
        If your model requires any Plugins, this is where you can load them.
        '''
       
        self.plugin = IECore()
        model_bin = os.path.splitext(self.model_name)[0] + ".bin"
        
        ### Load IR files into their related class
        self.network = IENetwork(model=self.model_name, weights=model_bin)
        
        # Add a CPU extension, if applicable
        if self.extensions and "CPU" in self.device:
            self.plugin.add_extension(self.extensions, self.device)
        
        ### Get the supported layers of the network
        supported_layers = self.plugin.query_network(network=self.network, device_name=self.device)
        
        ### Check for any unsupported layers, and let the user
        ### know if anything is missing. Exit the program, if so.
        unsupported_layers = [l for l in self.network.layers.keys() if l not in supported_layers]
        if len(unsupported_layers) != 0:
            print("Unsupported layers found: {}".format(unsupported_layers))
            print("Check whether extensions are available to add to IECore.")
            exit(1)
        
        ### Load the network into the Inference Engine
        self.exec_network = self.plugin.load_network(self.network, self.device)
        
        # Get the input layer
        self.input_blob = [x for x in self.network.inputs.keys()]
        self.output_blob = [x for x in self.network.outputs.keys()]

    def predict(self, left_eye, right_eye, head_pose_angle):
        '''
        TODO: You will need to complete this method.
        This method is meant for running predictions on the input image.
        '''
        left, right = self.preprocess_input(left_eye, right_eye)
        
        outputs = self.exec_network.infer({'head_pose_angles':head_pose_angle, \
                                           'left_eye_image':left, \
                                           'right_eye_image':right})
        
        mouse_coords, gaze_vec = self.preprocess_output(outputs, head_pose_angle[2])
        
        return mouse_coords, gaze_vec


    def check_model(self):
        pass

    def preprocess_input(self, left_eye, right_eye):
        '''
        Before feeding the data into the model for inference,
        you might have to preprocess it. This function is where you can do that.
        '''
        input_shape = self.network.inputs[self.input_blob[1]].shape
        
        img_left = cv2.resize(left_eye, (input_shape[3], input_shape[2]))
        img_left = np.transpose(np.expand_dims(img_left, axis=0), (0, 3, 1, 2))
        
        img_right = cv2.resize(right_eye, (input_shape[3], input_shape[2]))
        img_right = np.transpose(np.expand_dims(img_right, axis=0), (0, 3, 1, 2))
        return img_left, img_right

    def preprocess_output(self, outputs, angle):
        '''
        Before feeding the output of this model to the next model,
        you might have to preprocess the output. This function is where you can do that.
        '''
        vec = outputs[self.output_blob[0]][0]
        cosine = math.cos(angle*math.pi/180.0)
        sine = math.sin(angle*math.pi/180.0)
        
        x = vec[0] * cosine + vec[1] * sine
        y = -vec[0] *  sine + vec[1] * cosine

        return (x, y), vec
