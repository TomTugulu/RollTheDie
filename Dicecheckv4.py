# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 14:59:29 2019

@author: tuguluth
"""

'''
 * Python program to use contours to extract the dice in an image, to then add up totals.
'''
import cv2   #Key module allows me to check the number of dice
import sys   # Filepaths
import os    # Pip detection
import numpy as np
from imageai.Prediction.Custom import CustomImagePrediction

# read command-line arguments
filename = sys.argv[1]
t = int(sys.argv[2])

#Delete privious files if exist
for filenames in os.listdir("S:\Business Solutions\ThomasT\Current\Armoury\Macros\Dice"):
    if "sub" in filenames:
        os.remove(filenames)

# read original image
img = cv2.imread(filename)

#Use Masking of white areas to find the dice.
lower = np.array([175, 175, 175] )
upper = np.array([255, 255, 255])
shapeMask = cv2.inRange(img, lower, upper)

contours, hierachy = cv2.findContours(shapeMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# use the contours to extract each image, into a new sub-image
for (i, c) in enumerate(contours):
    (x, y, w, h) = cv2.boundingRect(c)
    # use slicing and the (x, y, w, h) values of the bounding
    # box to create a subimage based on this contour
    if y+h < 50:
        subImg = img[y : y + h, x : x + w, :]
        # save the subimage as sub-x.jpg, where x is the number
        # of this contour.
        cv2.imwrite("sub-{}.jpg".format(i), subImg)
cv2.imwrite("Imgcheck.jpg".format(i), shapeMask)   
 

#Set Dice Count
Ones = 0
Twos = 0
Threes = 0
Fours = 0
Fives = 0
Sixes = 0
UnknownDie = 0
z = 0
# Now we're looking to do pip detection on each image
    
# read original image

for filenames in os.listdir("S:\Business Solutions\ThomasT\Current\Armoury\Macros\Machine Learning"):
    if "sub" in filenames:
        filename = filenames
        
        print(filename)
        img = cv2.imread(filename)
        
        execution_path = os.getcwd()

        prediction = CustomImagePrediction()
        prediction.setModelTypeAsResNet()
        prediction.setModelPath("model_ex-105_acc-0.888889.h5")
        prediction.setJsonPath("dice_model_class.json")
        prediction.loadModel(num_objects=6)
        
        prediction, probabilities = prediction.predictImage(filename, result_count=1)                     
        for eachPrediction, eachProbability in zip(prediction, probabilities):
      
            prediction = int(eachPrediction)
            
            z = z+1
            if prediction == 1:
                Ones = Ones + 1
            elif prediction == 2:
                Twos = Twos + 1
            elif prediction == 3:
                Threes = Threes + 1
            elif prediction == 4:
                Fours = Fours + 1    
            elif prediction == 5:
                Fives = Fives + 1
            elif prediction == 6:
                Sixes = Sixes + 1
            else:
                UnknownDie = UnknownDie + 1
                z = z-1

print("Total Ones:", Ones)    
print("Total Twos:", Twos)              
print("Total Threes:", Threes)              
print("Total Fours:", Fours)              
print("Total Fives:", Fives)              
print("Total Sixes:", Sixes)              
print("Total Unknown Shapes:", UnknownDie)
print("Dice Rolled:", z)    