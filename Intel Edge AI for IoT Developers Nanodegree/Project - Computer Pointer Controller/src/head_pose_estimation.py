'''
This is a sample class for a model. You may choose to use it as-is or make any changes to it.
This has been provided just to give you an idea of how to structure your model class.
'''
import cv2
import os
import numpy as np
from openvino.inference_engine import IENetwork, IECore

class Model_Head_Pose_Estimation:
    '''
    Class for the Head Pose Estimation Model.
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
        res = self.preprocess_output(outputs)
        
        return res


    def check_model(self):
        pass

    def preprocess_input(self, image):
        '''
        Before feeding the data into the model for inference,
        you might have to preprocess it. This function is where you can do that.
        '''
        input_shape = self.network.inputs[self.input_blob].shape
        img = cv2.resize(image, (input_shape[3], input_shape[2]))
        img = np.transpose(np.expand_dims(img, axis=0), (0, 3, 1, 2))
        return img

    def preprocess_output(self, outputs):
        '''
        Before feeding the output of this model to the next model,
        you might have to preprocess the output. This function is where you can do that.
        '''
        results = []

        results.append(outputs['angle_y_fc'].tolist()[0][0])
        results.append(outputs['angle_p_fc'].tolist()[0][0])
        results.append(outputs['angle_r_fc'].tolist()[0][0])
        
        return results
