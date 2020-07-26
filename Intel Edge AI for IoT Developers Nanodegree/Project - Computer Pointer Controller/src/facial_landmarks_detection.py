'''
This is a sample class for a model. You may choose to use it as-is or make any changes to it.
This has been provided just to give you an idea of how to structure your model class.
'''
import cv2
import os
import numpy as np
from openvino.inference_engine import IENetwork, IECore

class Model_Facial_Landmarks_Detection:
    '''
    Class for the Facial Landmarks Detection Model.
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
        self.input_blob = next(iter(self.network.inputs))
        self.output_blob = next(iter(self.network.outputs))

    def predict(self, image):
        '''
        TODO: You will need to complete this method.
        This method is meant for running predictions on the input image.
        '''
        img_processed = self.preprocess_input(image)
        outputs = self.exec_network.infer({self.input_blob : img_processed})
        coords = self.preprocess_output(outputs)
        
        h = image.shape[0]
        w = image.shape[1]
        
        coords = (coords*np.array([w, h, w, h])).astype(np.int16)
        margin = 10
        left_eye = image[coords[1]-margin:coords[1]+margin, coords[0]-margin:coords[0]+margin]
        right_eye = image[coords[3]-margin:coords[3]+margin, \
                         coords[2]-margin:coords[2]+margin]
        eye_coords = [[coords[0]-margin,coords[1]-margin,coords[0]-margin,coords[1]+margin], \
                      [coords[2]-margin,coords[3]-margin,coords[2]-margin,coords[3]+margin]]
        return left_eye, right_eye, eye_coords


    def check_model(self):
        pass

    def preprocess_input(self, image):
        '''
        Before feeding the data into the model for inference,
        you might have to preprocess it. This function is where you can do that.
        '''
        input_shape = self.network.inputs[self.input_blob].shape
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (input_shape[3], input_shape[2]))
        img = np.transpose(np.expand_dims(img, axis=0), (0, 3, 1, 2))
        return img

    def preprocess_output(self, outputs):
        '''
        Before feeding the output of this model to the next model,
        you might have to preprocess the output. This function is where you can do that.
        '''
        out = outputs[self.output_blob][0]
        # leftx, lefty, rightx, righty
        return (out[0][0][0], out[1][0][0], out[2][0][0], out[3][0][0])
