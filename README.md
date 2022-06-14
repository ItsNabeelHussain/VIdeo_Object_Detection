# Video Object Detection
# Product Overview

Amazon Rekognition makes it easy to add image and video analysis to applications. You just provide an image or video to the Amazon Rekognition API, and the service can identify objects, people, text, scenes, and activities. It can detect any inappropriate content as well. Amazon Rekognition also provides highly accurate facial analysis and facial recognition. With Amazon Rekognition Custom Labels, you can create a machine learning model that finds the objects, scenes, and concepts that are specific to your business needs.

# Product Objectives

Similar to Amazon Rekognition, our product provides AI services in the domain of Computer Vision. It takes input of image or video and detects the objects in the provided input, and creates a documentation of what is in the input.

# Product Features

Product contains the following features:

Object Detection and Classification Text Detection and Text recognition Object Counting Person identification Celebrity recognition Object Detection and Classification

With the help of object detection and classification, users can find the info abo+ut the input whether there is any object existing in the input or not and if any exists then it classifies its class (return either its cat, dog, table or whatever).

Text Detection and recognition

Text detection and recognition can help to detect whether any text exists in the input or not, if text is detected then it can extract it. Currently only the English language is supported.

Object counting Object counting iis the technique that return the count of same type of object, for example consider the following image:

If user provide the above image as input it get the following output:

{ “Apple”: 2 “Banana”: 1 }

Person Identification

Person Identification extracts humans from the given input, for example if there is a person riding a bike, then the result contains a separate label for the person.

# Celebrity recognition

It is the extension to person identification, it check the results of person identification and process to check that whether there is any celebrity exist or not, if celebrity exist then it creates label with celebrity name and return final output.
