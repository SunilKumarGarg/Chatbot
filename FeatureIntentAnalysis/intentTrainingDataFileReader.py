import config
import re

class IntentDataFileReader:

    def __init__(self):
        
        f = open(config.INTENT_DATA_FILE)
        feature = ""
        intent = ""

        self.data = {}
        FeatureObject = []           

        lines = f.readlines()
        for line in lines:
            line = str.rstrip(str.lstrip(line))
            if "#END" in line:
                if feature != "":
                    self.data[feature] = FeatureObject                
                return
            else:                
                if re.match(r"^@.*", line):
                    line = re.search(r"^@(.*):", line)
                    if line != feature:
                        if feature != "":
                            self.data[feature] = FeatureObject
                            FeatureObject = []

                        feature = line.group(1)
                        

                elif re.match(r"^~.*:", line):
                    line = re.search(r"^~(.*):", line)
                    if line != intent:
                        #re.match()
                        intent = line.group(1)
                        
                elif len(line):
                    statement = line
                    FeatureObject.append((statement,intent))


    def getIntentTrainingData(self, feature):
        return self.data[feature]

