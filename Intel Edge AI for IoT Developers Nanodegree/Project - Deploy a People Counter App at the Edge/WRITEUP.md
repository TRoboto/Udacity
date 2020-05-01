# Project Write-Up

You can use this document as a template for providing your project write-up. However, if you
have a different format you prefer, feel free to use it as long as you answer all required
questions.

## Explaining Custom Layers

The process behind converting custom layers involves adding extensions to the model optimizer and the inference engine. In addition to the use of the model extension generator tool to create templates for the model optimizer extension. Then, the model optimizer is used to generate the IR files. After that, we add the CPU extension, compile and use the inference engine with the custom layer. Also, model optimizer filter out all the layers which are not in supported layer. And those are treated as custom layer. Adding a custom layer is dependent on the orginal framework: 1. Register an extension to model optimizer-- common for both 2. for Caffe: Register the layer as custom and then use caffe to calculate the output shape 3. Tensorflow: Replace unsupported subgraph with another subgraph



I used SSD Mobilenet v2 model which is obtained from [here]( https://docs.openvinotoolkit.org/latest/_docs_MO_DG_prepare_model_convert_model_Convert_Model_From_TensorFlow.html).

Here are the steps I used to get my model ready for inference:  
1- Downloaded the model using `wget`
2- Run the following code
`
python /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config pipeline.config --reverse_input_channels --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/ssd_v2_support.json 
`

Some of the potential reasons for handling custom layers arise from the fact that deep learning models have many different layers that are used nowadays. More new layers and architecture will definitely come up in the near future, thus the need for custom layers is essential if we need to benefit from our models. Also, it is possible that IR doesn't support all the layers from the original framework. Sometimes because of hardware, for example on cpu there are few IR model which are directly supported but others may not.

## Comparing Model Performance

My method(s) to compare models before and after conversion to Intermediate Representations
were:

I run the model on my Nvidia GTX 980m before tranforming it to the IR. The model was running in a good speed, I beileve this is because it uses layers for mobile, and I was able to detect all 6 people perfectly. However, running it using OpenVino led to more speed but it wasn't as accuarte as before.

The difference between model accuracy pre- and post-conversion was not quite big. The original model was able to detect all 6 persons with high confidence of about 80% while the IR model detected 7 persons with a confidence of about 72%, and also failed to detect one person while he was present for more than 5 seconds. 

The speed of the model before doing conversion was of average about 0.12 seconds while after doing conversion it decreased to 0.07 seconds which is about half, making it fast. This makes it run fast even on a CPU which is where I tested it! This makes it can run 14 fps on real hardware, which is not that bad. Also, we can run it on edge without having to deal with the high cost and high latency of the cloud serves.

The size of the model pre- and post-conversion was 66 MB and 64 MB respectivily. They were almost the same.

## Assess Model Use Cases

Some of the potential use cases of the people counter app are in places where one needs to count the number of people entered his place for statistical purposes, places like stores and resturants.

Each of these use cases would be useful because they allow for huge improvements in marketing strategies and also help in maximizing profits.

## Assess Effects on End User Needs

Lighting, model accuracy, and camera focal length/image size have different effects on a
deployed edge model. The potential effects of each of these are as follows:

* Bad lighing will definitly decrease the performance of the model.
* Model accuracy depends on the need of the user, if the user doesn't care that much about accuracy, meaning that he is okay with few messes, then accuracy is not a priority but it should be acceptable.
* Camera focal length and image size are really important, we need to make sure that the model is trained on the different focal length that it would face in the real world. Otherwise, the performance is going to be really bad.

## Model Research

[This heading is only required if a suitable model was not found after trying out at least three
different models. However, you may also use this heading to detail how you converted 
a successful model.]

In investigating potential people counter models, I tried each of the following three models:

- Model 1: Faster R-CNN Inception V2 COCO	
  - http://download.tensorflow.org/models/object_detection/faster_rcnn_inception_v2_coco_2018_01_28.tar.gz
  - I converted the model to an Intermediate Representation with the following arguments
  `python /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config pipeline.config --reverse_input_channels --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/faster_rcnn_support.json`
  
  - The model was insufficient for the app because it didn't work, I tried every possible solution provided by the mentors in the hub! there are two input layers which I correctly used the correct layer but the model doesn't work, it fails on wait function.
  
- Model 2: SSD Inception V2 COCO
  - http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_2018_01_28.tar.gz
  - I converted the model to an Intermediate Representation with the following arguments
  `python /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config pipeline.config --reverse_input_channels --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/ssd_v2_support.json
  `
  - The model was insufficient for the app because it failed to detect 2 persons in the video for the whole duration of their existence.
  - I tried to improve the model for the app by using the thrid model.

- Model 3: SSD Lite MobileNet V2 COCO
  - http://download.tensorflow.org/models/object_detection/ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz
  - I converted the model to an Intermediate Representation with the following arguments
  `python /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config pipeline.config --reverse_input_channels --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/ssd_v2_support.json
  `
  - The model was insufficient for the app because it also failed to detect 2 persons. It is also not that good as its confidenace of detection a person is somewhere low.
  - I tried to improve the model for the app by using SSD MobileNet V2 COCO which I found is the best model from the available zoo models.
