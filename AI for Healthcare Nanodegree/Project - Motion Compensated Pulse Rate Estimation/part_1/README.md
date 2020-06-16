## Part 1: Pulse Rate Algorithm Overview

### Algorithm Specifications
You must build an algorithm that:
  * estimates pulse rate from the PPG signal and a 3-axis accelerometer.
  * assumes pulse rate will be restricted between 40BPM (beats per minute) and 240BPM
  * produces an estimation confidence. A higher confidence value means that this estimate should be more accurate than an estimate with a lower confidence value.
  * produces an output at least every 2 seconds.  

### Success Criteria
Your algorithm performance success criteria is as follows: the mean absolute error at 90% availability must be less than 15 BPM on the test set.  Put another way, the best 90% of your estimates--according to your own confidence output-- must have a mean absolute error of less than 15 BPM. The evaluation function is included in the starter code.

Note that the unit test will call `AggregateErrorMetric` on the output of your `RunPulseRateAlgorithm` on a test dataset that you do not have access to. The result of this call must be less than 15 BPM for your algorithm's performance to pass. The test set should be easier than the training set so as long as your algorithm is doing reasonably well on the training data set it should pass this test.

**This will be validated through the Test Your Algorithm Workspace which includes a unit test.**

### Some Helpful Tips
  1. Remember to bandpass filter all your signals. Use the 40-240BPM range to create your pass band.
  2. Use plt.specgram to visualize your signals in the frequency domain. You can plot your estimates on top of the spectrogram to see where things are going wrong.
  3. When the dominant accelerometer frequency is the same as the PPG, try picking the next strongest PPG frequency if there is another good candidate.
  4. Sometimes the cadence of the arm swing is the same as the heart beat. So if you can't find another good candidate pulse rate outside of the accelerometer peak, it may be the same as the accelerometer.
  5. One option for a confidence algorithm is to answer the question, "How much energy in the frequency spectrum is concentrated near the pulse rate estimate?" You can answer this by summing frequency spectrum near the pulse rate estimate and dividing it by the sum of the entire spectrum.
  
### Dataset
You will be using the Troika<sup>1</sup> dataset to build your algorithm. Find the dataset under datasets/troika/training_data. The README in that folder will tell you how to interpret the data. The starter code contains a function to help load these files.

1. **Troika** - Zhilin Zhang, Zhouyue Pi, Benyuan Liu, ‘‘TROIKA: A General Framework for Heart Rate Monitoring Using Wrist-Type Photoplethysmographic Signals During Intensive Physical Exercise,’’IEEE Trans. on Biomedical Engineering, vol. 62, no. 2, pp. 522-531, February 2015. Link

### Getting Started
The starter code includes a few helpful functions. 
- `TroikaDataset`, `AggregateErrorMetric`, and `Evaluate` do not need to be modified.  
- Use `TroikaDataset` to retreive a list of .mat files containing reference and signal data. 
- Use `scipy.io.loadmat` to the .mat file into a python object. 
- The bulk of the code will be in the `RunPulseRateAlgorithm` function. You can and should break the code out into multiple functions. 
- `RunPulseRateAlgorithm` will take in two filenames and return a tuple of two numpy arrays--per-estimate pulse rate error and confidence values. Remember to write docstrings for all functions that you write (including `RunPulseRateAlgorithm`)
- Finally, run the `Evaluate` function to call your algorithm on the Troika dataset and compute an aggregate error metric. While building the algorithm you may want to inspect the algorithm errors on more detail.

### Folder Contents

#### Starter
These are the files that are given:
- `README.md`
- `datasets`
- `pulse_rate_starter.ipynb`

#### Completed
Once you have completed this portion these should be the files in this repo.
- `README.md`
- `datasets` - this folder should be removed when submitting for reviewers. 
- `pulse_rate.ipynb`<sup>*</sup> - complete pulse rate algorithm and write-up
- `unit_test.ipynb`<sup>*</sup> - includes the complete pulse rate algorithm 
- `passed.png`<sup>*</sup> - rendered in the `unit_test.ipynb` showing that the algorithm passed and by what error metric.


<sup>*</sup> These files can be named slightly different but must fufill the description given and be clear to the reviewer what that file includes.
