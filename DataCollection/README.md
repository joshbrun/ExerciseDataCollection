# ExerciseDataCollection
ExerciseDataCollection is the preprocessing system for our BE(Hons) honors project. Automatic system to download, extract, process and create trainable models via skeletal mapping via OpenPose. 

# Sequential Pipeline  

## Video Identification  
The first step is to locate and label youtube videos, and sub clips within these videos which corresspond to correct form within a particual exercise.

## Video Downloading  
Automatically downloading videos when the system is run, skipping videos which have already been downloaded on the local system.
This is done via the youtube-dl python module.

## Frame Extraction  
Automatically split the videos into a set of images, each set corresponding to a stage of a particular exercise. Labeling them either as good form or bad form.

## Skeletal Mapping  
Using OpenPose extract skeletal information from the frames. 

## Normalize  
Use a normalization method on the skeletal graph.

## Create Trainable Data Sets  
Combine relevent frames into various datasets, ready to train classfication models.
