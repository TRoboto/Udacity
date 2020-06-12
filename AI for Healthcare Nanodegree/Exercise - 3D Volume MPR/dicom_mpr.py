#%%
import pydicom
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt

# TASK: In the same folder as this .py file you will find a DICOM folder
# with a volume in it. You can assume that all files belong to the same series.
# Your task is to visualize any three slices across the three 
# cardinal planes from this volume: Axial, Coronal and Sagittal. You can visualize 
# by saving them as png, similar to the previous exercise. You can visualize slice at 
# any level, but I suggest that you visualize slices located in the middle of the volume.

# 
# Bonus points: 
# 1) What is the modality that you are dealing with here?
# 2) Try to figure out which axis corresponds to what plane by searching online.
# You should have a good guess of what anatomy you are looking at if you visualize the middle slice
# 3) Try plotting the slices in non-primary planes with proper aspect ratio
#
# Hints:
# - You may want to rescale the output because your voxels are non-square. 
# - Don't forget that you need to order your slices properly. Filename 
# may not be the best indicator of the slice order. 
# If you're confused, try looking up the first value of ImagePositionPatient
# - Don't forget the windowing. A good initial guess would be scaling all
# image values down to [0..1] range when saving. Pillow deals with such well

# %% 
# Load the volume into array of slices
path = f"volume"
slices = [pydicom.dcmread(os.path.join(path, f)) for f in os.listdir(path)]

# What are the dimensions?
print(f"{len(slices)} of size {slices[0].Rows}x{slices[0].Columns}")

# What is the modality? 
print(f"Modality: {slices[0].Modality}")

# %%
# What is the slice spacing?
print(f"Pixel Spacing: {slices[0].PixelSpacing}, slice thickness: {slices[0].SliceThickness}")

# Load into numpy array
image_data = np.stack([s.pixel_array for s in slices])
print(image_data.shape)

# %%
print("Saving axial: ")
# Extract slice
axial = image_data[image_data.shape[0]//2]
plt.imshow(axial, cmap="gray")
# Save using full-range window
im = Image.fromarray((axial/np.max(axial)*0xff).astype(np.uint8), mode="L")
im.save("axial.png")


# %%
print("Saving sagittal: ")
# Extract slice
sagittal = image_data[:,:, image_data.shape[2]//2]
# Compute aspect ratio
aspect = slices[0].SliceThickness / slices[0].PixelSpacing[0]
print(sagittal.shape)
plt.imshow(sagittal, cmap="gray", aspect = aspect)
# Save using full-range window
im = Image.fromarray((sagittal/np.max(sagittal)*0xff).astype(np.uint8), mode="L")
im = im.resize((sagittal.shape[1], int(sagittal.shape[0] * aspect)))
im.save("sagittal.png")

# %%
print("Saving coronal: ")
# Extract slice
coronal = image_data[:, image_data.shape[1]//2, :]
# Compute aspect ratio
aspect = slices[0].SliceThickness / slices[0].PixelSpacing[0]
print(coronal.shape)
plt.imshow(coronal, cmap="gray", aspect = aspect)
# Save using full-range window
im = Image.fromarray((coronal/np.max(coronal)*0xff).astype(np.uint8), mode="L")
im = im.resize((coronal.shape[1], int(coronal.shape[0] * aspect)))
im.save("coronal.png")