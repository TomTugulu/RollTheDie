# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 11:13:15 2019

@author: tuguluth
"""

from imageai.Prediction.Custom import ModelTraining

model_trainer = ModelTraining()
model_trainer.setModelTypeAsResNet()
model_trainer.setDataDirectory("idendice")
model_trainer.trainModel(num_objects=6, num_experiments=200, enhance_data=True, batch_size=10, show_network_summary=True)