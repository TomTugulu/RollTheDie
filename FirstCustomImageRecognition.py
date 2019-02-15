# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 07:52:48 2019

@author: tuguluth
"""

from imageai.Prediction.Custom import CustomImagePrediction
import os

execution_path = os.getcwd()

prediction = CustomImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath("model_ex-105_acc-0.888889.h5")
prediction.setJsonPath("dice_model_class.json")
prediction.loadModel(num_objects=6)

predictions, probabilities = prediction.predictImage("Testcase7.jpg", result_count=3)

for eachPrediction, eachProbability in zip(predictions, probabilities):
    print(eachPrediction , " : " , eachProbability)