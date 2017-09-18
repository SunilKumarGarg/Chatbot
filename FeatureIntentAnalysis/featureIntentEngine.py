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
        self.webProductData = WebProductData(domain)
        self.featureValues = self.getFeatureValue(Feature, product)
        
        self.product = product
        self.Feature = Feature
        


    def getInputArray(self, var):        
        bagOfWords = IntentTrainingData.bagOfWords(self.Feature)
        listIntent = IntentTrainingData.liftOfIntent(self.Feature)
        filteredData = TockenizeData.getTockenizedDataWithStem(var)

        localTrainingSet = []
        for word in bagOfWords:        
            if word in filteredData:
                localTrainingSet.append(1)
            else:
                localTrainingSet.append(0)

        return localTrainingSet


    def getIntentAndValue(self, statement):
        filteredData = TockenizeData.getTockenizedDataWithStem(statement)


        Input = self.getInputArray(statement)        

        if len(filteredData) == 1:
            for f in self.getFeatureValue(self.Feature, self.product):
                if filteredData[0] in f:
                    #print "great choice"
                    return "like", filteredData[0]

        var = Dataconverter.convertBinaryListToInt(IntentTrainingData.model[self.Feature].predict([Input]))

        filteredData = TockenizeData.getTockenizedData(statement)
        listIntent = IntentTrainingData.liftOfIntent(self.Feature)        
        
        intent = listIntent[var]
        featureValue = ""

        print filteredData
        print self.featureValues
        print intent
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


if __name__ == "__main__":    
    IntentTrainingData.initialize()
    inAnaly = IntentAnalyzer("size","shoes","amazon.com")
    while(1):
        var = raw_input(">>")
        intent, featureValue = inAnaly.getIntentAndValue(var)
        print "you " + intent + " " + featureValue
    