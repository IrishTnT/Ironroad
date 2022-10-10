from turtle import clear
import requests
import json
import re
import xml.etree.ElementTree as ET
import urllib
import numpy

# Gets which train type the User wishes to read.
type = input("What type of train do you wish to search for?\nM - Mainline,\nD - DART,\nS- Suburban,\nA - All.\n(Any other input will search all trains.)\n")

if type.upper() == "M":
    print("Selected MAINLINE trains. Please wait...")
    requestURL = 'http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML_WithTrainType?TrainType=M'
elif type.upper() == "D":
    print("Selected DART trains. Please wait...")
    requestURL = 'http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML_WithTrainType?TrainType=D'
elif type.upper() == "S":
    print("Selected SUBURAN trains. Please wait...")
    requestURL = 'http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML_WithTrainType?TrainType=S'
elif type.upper() == "A":
    print("Selected ALL trains. Please wait...")
    requestURL = 'http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML_WithTrainType?TrainType=A'
else:
    print("Defaulted to ALL trains. Please wait...")
    requestURL = 'http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML_WithTrainType?TrainType=A'

root = ET.parse(urllib.request.urlopen(requestURL)).getroot()

# urllib.request.urlopen() is used to request the data using the api
# et.parse turns it into an element
# getroot() will grab the root element and toss away any metadata


trainData = []

for child in root:
    # loops through all child elements of root (in this case "objTrainPositions")
    temp = {}
    # will create an empty object for each itiration of the loop
    for data in child:
        # Loops through all child elements of each train 
        # print(data.tag.split('}'))
        # data.tag will return the name of the tag ("desination", "traindate" etc)
        # The tags appear as "{url} name" so i split the string into an array at the character "}"
        temp[data.tag.split("}")[1]] = data.text
        # selects the second element in the array "['{url}', 'name']" and will create an key in the temp
        # object with the name of the tag and the value will be the text in the tag
    trainData.append(temp)
    # will add the object to the trainData array

# print(trainData)
with open("./test.json", "w") as f:
    f.write(json.dumps(trainData, indent = 4, sort_keys = True))
    # This just dumps the data into a json file

# Find the train you want
dest = input("Loaded timetables.\nSelect your destination, or type 'cancel' to exit.\n")

def extract_train_data(destination):
    train = []
    
    ##for iterator in trainData:
        
    
    train = next((item for item in trainData if item["Direction"].lower() == destination.lower()), None)
    
    if train:
        return train["PublicMessage"].replace('\\n', '\n').splitlines()
    return "N/A"

while extract_train_data(dest) == "N/A":
    if dest == "cancel":
        exit()
        
    if dest[0].lower() + dest[1].lower() == "to":
        print("Train", dest, "not found!")
    else:
        print("Train to", dest, "not found!")
    dest = input("Select your destination, or type 'cancel' to exit.\n ")

if extract_train_data(dest) != "N/A":
    print("The next train is the", extract_train_data(dest)[1], "[" + extract_train_data(dest)[0] + "].", extract_train_data(dest)[2] + ".")