import sys
sys.path.append('../Data')
sys.path.append('../WebDataParser')
sys.path.append('../Utility')

import numpy as np
import tflearn
import tensorflow as tf
from featureIntentData import *
from tockenizeData import *
from Dataconverter import *
from webProductData import *
from json import dumps



class IntentAnalyzer:

    def __init__(self, Feature, product, domain):
        self.trainingData = IntentTrainingData(Feature)
        self.webProductData = WebProductData(domain)
        self.featureValues = self.getFeatureValue(Feature, product)
        
        self.product = product
        self.Feature = Feature
        self.trainModel()


    def getInputArray(self, var):        
        bagOfWords = self.trainingData.bagOfWords()
        listIntent = self.trainingData.liftOfIntent()
        filteredData = TockenizeData.getTockenizedData(var)

        localTrainingSet = []
        for word in bagOfWords:        
            if word in filteredData:
                localTrainingSet.append(1)
            else:
                localTrainingSet.append(0)

        return localTrainingSet


    def getIntentAndValue(self, statement):
        filteredData = TockenizeData.getTockenizedData(statement)


        Input = self.getInputArray(statement)        

        if len(filteredData) == 1:
            for f in self.getFeatureValue(self.Feature, self.product):
                if filteredData[0] in f:
                    #print "great choice"
                    return "like", filteredData[0]

        var = Dataconverter.convertBinaryListToInt(self.model.predict([Input]))

        filteredData = TockenizeData.getTockenizedData(statement)
        listIntent = self.trainingData.liftOfIntent()        
        
        intent = listIntent[var]
        featureValue = ""

        for value in self.featureValues:
            if value in filteredData:
                featureValue = value
                #print "great choice"
                return intent, featureValue

        #print "Sorry, we do not have this selection." 
        return "none", ""
        
        

    def getFeatureValue(self,feature, product):
        return self.webProductData.getFeatureInfo({"product_list.product": product }, feature)

    def question(self):
        return dumps({"Text": "Please select " + self.Feature, "Button" :str(self.getFeatureValue(self.Feature, self.product))})




    def trainModel(self):

        train_x, train_y = self.trainingData.getTrainingSet()        
        tf.reset_default_graph()
        net = tflearn.input_data(shape=[None, 22])
        net = tflearn.fully_connected(net, 32)
        net = tflearn.fully_connected(net, 32)
        net = tflearn.fully_connected(net, 2, activation='softmax')
        net = tflearn.regression(net)

        # Define model and setup tensorboard
        self.model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
        # Start training (apply gradient descent algorithm)
        self.model.fit(train_x, train_y, n_epoch=500, batch_size=16, show_metric=True)


if __name__ == "__main__":    
    
    inAnaly = IntentAnalyzer("color","shoes","amazon.com")
    while(1):
        var = raw_input(">>")
        intent, featureValue = inAnaly.getIntentAndValue(var)
        print "you " + intent + " " + featureValue
    