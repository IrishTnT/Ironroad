# This is legacy spaghetti code prior to the 0.2.X re-write.
# Features are still being carried over, and this file exists
# for archival reasons.
# It's missing core 0.2.X features, and Ironroad.py is recommended
# over IrishRail.py

from turtle import clear
import requests
import json
import re
import xml.etree.ElementTree as ET
import urllib
import numpy

version = "v0.1.1"

## To-Do:
# -> Show all trains on [T]
# -> Fix input checks on [T]
# -> Stop errors.
# -> Do error correction on [T]
# -> Choose Depart & Arrive [S]

print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print("@@@@@@@@@@@,,,((@@@@@@@@@@@***@@@@@@@@@@")
print("@@@@@@@@@*****(////@@@@@@@@*****@@@@@@@@")
print("@@@@@@//******/┏━━━━━━━━┓@@*******/@@@@@")
print("@@@@//////****/┃IRONRAIL┃@@*******///@@@")
print("@(((/////////*/┃   by   ┃..*******//////")
print("@@############@┃IrishTnT┃..****//////((@")
print("@@@@@#########@┗━━━━━━━━┛..****/////@@@@")
print("@@@@@@@@######@@@@@@@..... ****//@@@@@@@")
print("@@@@@@@@@@%%%%@@@@@@@@@..  ****@@@@@@@@@")
print("@@@@@@@@@@@@@%@@@@@@@@@@@@ *@@@@@@@@@@@@")
print("IRONRAIL by IrishTnT |", version)
print("\t    IrishTnT.com\n\n")


# This is the input, deciding where the next input will take the user
mreq = input("Which do you want to query?\nS - Stations,\nT - Trains.\n(Any other input will search for Trains.)\n")

if mreq.upper() == "S":
    print("\n\n---==<[STATIONS]>==---")
    tloc = 0
elif mreq.upper() == "T":
    print("\n\n---==<[TRAINS]>==---")
    tloc = 1
else:
    print("\n\n---==<[TRAINS]>==---")
    tloc = 1

# [T] Train type inputs
if tloc == 1:
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
elif tloc == 0: # [S] Station Query
    sparseloop = 0
    stype = input("What station do you want to query\n")
    
    while sparseloop == 0:
        if len(stype) < 4:
            stype = input("<STATION NAME MUST BE 4 LETTERS OR LONGER!>\nWhat station do you want to query\n")
        
        requestURL = 'https://api.irishrail.ie/realtime/realtime.asmx/getStationsFilterXML?StationText='+stype.replace(' ', '%20')
        root = ET.parse(urllib.request.urlopen(requestURL)).getroot()
        
        stationdata = []
        
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
            stationdata.append(temp)
            # will add the object to the trainData array
        if stationdata == []:
            stype = input("<STATION NOT FOUND!>\nWhat station do you want to query\n")
        elif len(stationdata) > 1:
            print("MULTIPLE STATIONS FOUND!")
            i = 0
            iterdata = iter(item for item in stationdata)
            
            while i < len(stationdata):
                station = next((iterdata))
                print(str(i) + ".", station["StationDesc"])
                i = i + 1
            stype = input("Please enter Station name!\n")
            
        else:
            break
        
    
    stime = input("How far into the future do you want to query? (5 - 90 mins)\n")
    
    # Ensuring that the user can repeatedly
    # enter invalid values and will only
    # continue when a correct value is entered
    while sparseloop == 0:
        if "." in stime:
            stime = input("<WHOLE NUMBERS ONLY!>\nHow far into the future do you want to query? (5 - 90 mins)\n")
        elif stime.isdigit() == False:
            stime = input("<NUMBERS ONLY!>\nHow far into the future do you want to query? (5 - 90 mins)\n")
        elif int(stime) < 5:
            stime = input("<TIME TOO SHORT!>\nHow far into the future do you want to query? (5 - 9 mins)\n")
        elif int(stime) > 90:
            stime = input("<TIME TOO LONG!>\nHow far into the future do you want to query? (5 - 90 mins)\n")
        else:
            break

    requestURL = 'https://api.irishrail.ie/realtime/realtime.asmx/getStationDataByNameXML_withNumMins?StationDesc=' + stype.replace(' ', '%20') + '&NumMins=' + stime
    print("Querying", stype.upper() + ",", stime, "minutes into the future. Please wait...")

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

#print(trainData)
with open("./test.json", "w") as f:
    f.write(json.dumps(trainData, indent = 4, sort_keys = True))
    # This just dumps the data into a json file

if tloc == 0:
    
    if trainData == []:
        print("No trains found, or the station does not exist.")
        exit()
    else:
        train = []

        i = 0
        iterdata = iter(item for item in trainData)
        
        while i < len(trainData):
            train = next((iterdata))
            
            if train["Locationtype"].lower() == "s" or train["Locationtype"].lower() == "d":
                intype = "arriving in"
            elif train["Locationtype"].lower() == "o":
                intype = "departing in"
                
            if int(train["Late"]) < 0:
                ## This next line is plague-inducing. It's really bad, but its is REQUIRED.
                runningtype = "".join(("Running ", str(abs(int(train["Late"]))), " minutes early."))
            elif int(train["Late"]) == 0:
                runningtype = "Running on time."
            else:
                runningtype = "".join(("Running ", train["Late"], " minutes late."))
            
            if int(train["Duein"]) != 1:
                print("Train from", train["Origin"], "to", train["Direction"], intype, train["Duein"], "minutes.", str(runningtype))
            else:
                print("Train from", train["Origin"], "to", train["Direction"], intype, train["Duein"], "minute.", str(runningtype))
                
            i = i + 1

elif tloc == 1:
    # Find the train you want
    dest = input("Loaded timetables.\nSelect your destination, or type 'cancel' to exit.\n")

    def extract_train_data(destination):
        train = []
        
        ##for iterator in trainData:
        train = next((item for item in trainData if item["Direction"].lower() == destination.lower()), None)
        
        if train:
            return train["PublicMessage"].replace('\\n', '\n').splitlines()
        return None

    while extract_train_data(dest) == None:
        if dest == "cancel":
            exit()
            
        if dest[0].lower() + dest[1].lower() == "to":
            print("Train", dest, "not found!")
        else:
            print("Train to", dest, "not found!")
        dest = input("Select your destination, or type 'cancel' to exit.\n ")

    if extract_train_data(dest) != None:
        print("The next train is the", extract_train_data(dest)[1], "[" + extract_train_data(dest)[0] + "].", extract_train_data(dest)[2] + ".")
