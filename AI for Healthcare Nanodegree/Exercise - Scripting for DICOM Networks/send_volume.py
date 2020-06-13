# In this exercise you will use your knowledge of DICOM and DICOM networking 
# to analyze an MR study on disk (this code could be running as a part of an AI server software), 
# select the series to process and send this series to a DICOM SCP 
# (which could be running your AI algorithm!)

# Your job is to complete this code so that it becomes a Python program that 
# takes in a name of the directory representing an MR study that contains subdirectories 
# representing MR series. Then you will select series that contain a "FLAIR" sequence
# and send that on to a DICOM SCP that will store it in the directory of your choice. 
# Use storescp command with the following syntax to bring up your SCP:
#
# sudo storescp 109 -v -aet TESTSCP -od <YOUR_DIRECTORY>
#
# Use storescu command to send the files. Use the provided os_command function to issue a
# command line with storescu
#
# The data that you need to send is in ./data directory. You might want to use dcmdump to 
# take a look at DICOM files and figure out what would be a good way to distinguish 
# FLAIR sequence from others. There is more than one way.

import os
import pydicom
import sys
import numpy as np
import subprocess

def os_command(command):
    # Comment this if running under Windows
    sp = subprocess.Popen(["/bin/bash", "-i", "-c", command])
    sp.communicate()

    # Uncomment this if running under Windows
    # os.system(command)

if __name__ == "__main__":
    
    dicom_path = sys.argv[1]

    if not os.path.isdir(dicom_path):
        exit("Expecting valid directory as first argument")

    # TASK: Your code here

    pass