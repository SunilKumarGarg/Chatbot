from flask import Flask, render_template, request, redirect, url_for
import sys

sys.path.append('Chatbot')
sys.path.append('SalespersonChatbot')
sys.path.append('featureDetection')
sys.path.append('FeatureIntentAnalysis')
sys.path.append('WebDataParser')
sys.path.append('Utility')
sys.path.append('Data')

from featureDetection import FeatureDetection
from chatbot import Chatbot
from uniqueID import UniqueID
from featureIntentData import IntentTrainingData
from featureDetection import FeatureDetectionEngine

app = Flask(__name__)
IntentTrainingData.initialize()
FeatureDetectionEngine.initialize()

#chatPerson = Chatbot("amazon.com")

userDatabase = {}


@app.route('/' , methods=['POST'])
def Welcome():
    p = request.get_json()
    uniqueID = UniqueID.getUniqueID()
    userDatabase[uniqueID] = Chatbot(p["Domain"])
    return userDatabase[uniqueID].greeting()

@app.route('/Input' , methods=['POST'])
def processInput():
    p = request.get_json()
    try:
        uniqueID = p["userID"]
    except:
        dumps({"Error": "Cannot Connect. Please close chat window and reopen."})

    print uniqueID
    return userDatabase[uniqueID].processInput(p)

if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=5001)