# Expected results

Please put the artefacts from Section 2 here:  
  
* Functional code that trains the segmentation model
* Test report with Dice scores on test set (can be json file). Your final average Dice with the default model should be around .90
* Screenshots from your Tensorboard (or other visualization engine) output, showing Train and Validation loss plots, along with images of the predictions that your model is making at different stages of training
* Your trained model PyTorch parameter file (model.pth)

## Suggestions for making your project stand out

* Can you write a 1-page email explaining what your algorithm is doing to a clinician who will be trying it out, but whom you never met? Make sure you include performance characteristics with some images. Try using their language and think of what would be the important information that they are looking for?
* Implement additional metrics in the test report such as Jaccard score, sensitivity or specificity. Think of what additional metrics would be relevant.
* In our dataset we have labels of 2 classes - anterior and posterior segments of the hippocampus. Can you train a version of model that segments the structure as a whole, only using one class? Is the performance better, the same or worse?
* Write up a short report explaining requirements for your training process (compute, memory) and suggestions for making it more efficient (model architecture, data pipeline, loss functions, data augmentation). What kind of data augmentations would NOT add value?
* What are best and worst performing volumes? Why do you think that's the case?
