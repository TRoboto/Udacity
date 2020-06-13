# In this exercise you will compute some of the performance metrics we have discussed
# Specifically, you will compute Sensitivity and Dice scores 
# between the ground truth for the volume from the previous lesson and the segmentation
# that your network had created. 
# Alternatively, there is a second, auto-generated segmentation available for you to 
# compare against
#
# Below we provide some starter code and put comments prepended with TASK to indicate 
# places where you need to fill in

import numpy as np
import nibabel as nib

if __name__ == "__main__":

    # TASK: Load segmentation masks from the nifti files in the folder data,
    # plus your own mask if you have created one in the previous exercise
    # spleen1_label_gt is the ground truth mask
    # spleen1_label_auto is the auto-generated one
    
    # <YOUR CODE HERE>
    # __SOLUTION
    lbl1 = nib.load("data/spleen1_label_auto.nii.gz").get_fdata()
    lbl2 = nib.load("data/spleen1_label_gt.nii.gz").get_fdata()
    # __SOLUTION

    # TASK: Now, implement two similarity metrics - sensitivity (assuming that gt is the True mask)
    # and Dice Similarity Coefficient. 
    # Hint: the formal measure of "set cardinality" that is featured in DSC definition could
    # be computed as simply the volume of your 3D object

    # <YOUR CODE HERE>
    # __SOLUTION
    def dsc3d(a,b):
        intersection = np.sum(a*b)
        volumes = np.sum(a) + np.sum(b)

        if volumes == 0:
            return -1

        return 2.*float(intersection) / float(volumes)

    print(f"DSC: {dsc3d(lbl1, lbl2)}")

    def sensitivity(gt,pred):
        # Sens = TP/(TP+FN)
        tp = np.sum(gt[gt==pred])
        fn = np.sum(gt[gt!=pred])

        if fn+tp == 0:
            return -1

        return (tp)/(fn+tp)

    print(f"Sensitivity: {sensitivity(lbl1, lbl2)}")