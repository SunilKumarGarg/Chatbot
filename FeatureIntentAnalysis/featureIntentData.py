from tockenizeData import *
import random
import numpy as np
from Dataconverter import *
from intentTrainingDataFileReader import *


class IntentTrainingData:

    
    def __init__(self, feature):
        self.readIntentTrainingData(feature)

    def readIntentTrainingData(self, feature):
        self.trainingData = IntentDataFileReader().getIntentTrainingData(feature)   


    def getFilteredTrainingData(self):
        FilteredTrainingSet = []

        for statement, intent in self.trainingData:
            f = TockenizeData.getTockenizedData(statement)
            FilteredTrainingSet.append((f, intent))

        return FilteredTrainingSet
    

    def bagOfWords(self):
        FilteredTrainingSet = self.getFilteredTrainingData()
        
        listElements = []
        for elements, intent in FilteredTrainingSet:
            for element in elements:
                listElements.append(element)
        
        return list(set(listElements))

    def liftOfIntent(self):
        FilteredTrainingSet = self.getFilteredTrainingData()
        listIntent = []
        for elements, intent in FilteredTrainingSet:
            listIntent.append(intent)

        return list(set(listIntent))


    def getTrainingSet(self):
        FilteredTrainingSet = self.getFilteredTrainingData()
        bagOfWords = self.bagOfWords()
        listIntent = self.liftOfIntent()
        
        trainingSet = []

        for wordCollection, intent in FilteredTrainingSet:
            localTrainingSet = []
            for word in bagOfWords:
                if word in wordCollection:
                    localTrainingSet.append(1)
                else:
                    localTrainingSet.append(0)
            
            trainingSet.append([localTrainingSet, Dataconverter.convertIntToBinaryList(listIntent.index(intent), len(listIntent))])    
            
            
        random.shuffle(trainingSet)
        features = np.array(trainingSet)

        # create train and test lists
        train_x = list(features[:,0])
        train_y = list(features[:,1])

        return train_x, train_y