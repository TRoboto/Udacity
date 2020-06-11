# FDA  Submission

**Your Name:** Mohammad Al-Fetyani

**Name of your Device:** PneumoniaNet 

## Algorithm Description 

### 1. General Information

**Intended Use Statement:**  
This model is intended for use on men and women from 1 to 85 years old who have no previous illnesses or who have one or a combination of the following diseases: atelectasis, heart enlargement, standardization, edema, effusion, emphysema, fibrosis, hernia, infiltration, mass, Creed, pleura thickening and pneumothorax

**Indications for Use:**  
Screening for pneumonia to assist radiologists in non-emergency situations.

**Device Limitations:**  
Requires at least a computer with 2-cores CPU and 8 GB RAM.

**Clinical Impact of Performance:**  
The algorithm is designed for high precision predictions. This means that when the algorithm predicts positive, the patient is more likely to have pneumonia. However, the algorithm tends to misclassify many positive cases as patients who have pneumonia may be classified as having no pneumonia.

### 2. Algorithm Design and Function

The algorithms uses deep neural network, spcificly VGG-16 architacture to classify the presece of pnuemonia from xray images. The flow starts with image prepcossing where all images are normalized, then the image is fed to the neural network and the network outputs a probability of having pneumonia. If the output probabilty is higher than a predefined threshold, it is classified as positive.

**DICOM Checking Steps:**  
It is guaranteed that DICOM only contains chest x-rays.  

**Preprocessing Steps:**  
ِImages are resized to 224x224, converted to RGB color channels and normalized to range of [0,1]

**CNN Architecture:**
The base network is VGG-16 pretrained on ImageNet dataset, followed by:
* Batch Normalization
* Conv2d layer with 1x1 kernal, 1024 filters, stride of 1 and relu activation fucntion.
* Dropout of 0.5
* Batch Normalization
* Conv2d layer with 1x1 kernal, 256 filters, stride of 1 and relu activation fucntion.
* Dropout of 0.5
* 7x7 AveragePooling2D layer
* Batch Normalization
* Conv2d layer with 1x1 kernal, 1 filter, stride of 1 and signmoid activation fucntion.
* Reshape to [batch_size, 1]

### 3. Algorithm Training

**Parameters:**
* Types of augmentation used during training
    * Horizontal flip
    * Random height shift of (+/-)10% of the image max.
    * Random width shift of (+/-)10% of the image max.
    * Random rotation shift of (+/-)20 degrees max.
    * Random shear shift of (+/-)10% max.
    * Random zoom of (+/-)10% max.
* Batch size = 64
* Optimizer learning rate = 1e-3
* Layers of pre-existing architecture that were frozen: first 17 layers.
* Layers of pre-existing architecture that were fine-tuned: dense layers of the vgg16 model and all followed layers.
* Layers added to pre-existing architecture: described above.

<img src="loss.png" />

<img src="auc.png" />

<img src="pc.png" />

**Final Threshold and Explanation:**  
The final threshold is 0.41 because it gives the highest precision

### 4. Databases

The dataset is obtained from [Kaggle](https://www.kaggle.com/nih-chest-xrays/data). The dataset contians 112,120 chest xray images with 1024x1024 resolution. It contains 14 diseases: atelectasis, heart enlargement, standardization, edema, effusion, emphysema, fibrosis, hernia, infiltration, mass, Creed, pleura thickening, pneumothorax and pneumonia. The figure below shows their distribution. It is to be noted that an image may contain multiple diseases.

<img src="dis_dis.png" />

The age distribution for people with pneumonia is presented below.

<img src="age.png" />

There are 1431 samples with pnuemonia and 110689 samples without pnuemonia in the dataset. The gender distribution is shown below with 56.5% male and 43.5% female.

<img src="sex.png" />



**Description of Training Dataset:** 
The training dataset is resampled with replacement to have 50% positive cases of pneumonia and 50% with no pneumonia. The total number of images in the training set becomes 2290 images.

**Description of Validation Dataset:** 
The validation set has 20% positive cases of pneumonia and 80% with no pneumonia. The total number of images in the validation set is 1430 images.

### 5. Ground Truth
The labels are obtained using NLP approach from the radiologist reports. They are expected to be accurate enough.


### 6. FDA Validation Plan

**Patient Population Description for FDA Validation Dataset:**

**Ground Truth Acquisition Methodology:**  
X-ray images validated be 3 different radiologists.

**Algorithm Performance Standard:**  
Precision
