import sys

from webProductData import *
from featureEngine import *
from featureDetection import FeatureDetection
from json import dumps
import json


class SalespersonChatbot:

    def __init__(self, domain): 
        self.webProductData = WebProductData(domain)
        self.domain = domain
        self.product = False
        
        self.productList = self.webProductData.getProductList()
        self.featureDetect = FeatureDetection()

    def getProductList(self):
        self.product = True
        prod = {}
        prod["Text"] = "Product List"
        prod["Button"] = self.productList
        return dumps(prod)

    def createFeatureInstance(self,product):
        self.product = False
        if product not in self.productList:
            print "Website does not sell " + product
            return -1

        self.featureInstance = []
        self.featureList = self.webProductData.getFeatureList({"product_list.product": product })

        for feature in self.featureList:
            self.featureInstance.append(FeatureEngine(feature, product, self.domain))

    def output(self, intent, result):  
      
        for featureObject in self.featureInstance:
                if featureObject.isSlothasValue() == False:
                    self.featureDetect.setcontext(featureObject.feature)
                    r = json.loads(featureObject.getQuestion())
                    r["Intent"] = intent
                    r["result"] = result

                    return dumps(r)


        
        print "You have selected this: "
        for featureObject in self.featureInstance:
            print featureObject.feature + ":"+featureObject.slot

        return self.createFinalResponse()

    def input(self, statement):
        feature = self.featureDetect.getFeature(statement)
        for fObject in self.featureInstance:
            if fObject.feature == feature:
                intent, value = fObject.getIntentAndValue(statement)
                return (intent, value)

    def processInput(self,statement):
        intent, result = self.input(statement)
        return self.output(intent, result)

    def createFinalResponse(self):
        res = {}
        feature = {}
        for featureObject in self.featureInstance:
            print featureObject.feature + ":"+featureObject.slot
            feature[featureObject.feature] = featureObject.slot

        res["Feature"] = feature
        print dumps(res)
        return dumps(res)
                
                    