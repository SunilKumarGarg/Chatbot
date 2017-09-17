import sys
sys.path.append('../Utility')

from tockenizeData import TockenizeData

class FeatureDetection:
    
    def __init__(self):
        self.feature = ""

    def getFeature(self, statement):
        
        innn = TockenizeData.getTockenizedData(statement)
        for i in innn:
            if i in ["red","blue","green"]:
                return "color"
            elif i in ["small", "medium", "size"]:
                return "size"
            elif i in ["adida", "rebook"]:
                return "brand"
            elif self.feature != "":
                return self.feature

    def setcontext(self, feature):
        self.feature = feature