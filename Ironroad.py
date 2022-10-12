from turtle import clear, goto
from thefuzz import fuzz
from thefuzz import process
import requests
import json
import re
import xml.etree.ElementTree as ET
import urllib
import numpy
from pathlib import Path

debug = 0 # This will show extra information on what the code is doing, turn to 0 for a more User-friendly console experience.
version = "v0.2.1"

aSP = Path("./allstations.json")
if aSP.is_file():
    if debug == 1:
        print("allstations.json exists")
else:
    if debug == 1:
        print("allstations.json doesn't exist. Grabbing.")
    parsed = []

    root = ET.parse(urllib.request.urlopen("http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML")).getroot()
    if debug == 1:
        print("API returned, parsing...")
    
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
        parsed.append(temp) # Adds temp to the array.
    
    if debug == 1:
        print("Parse complete. Writing allstations.json")
    with open("allstations.json", "w") as f:
        f.write(json.dumps(parsed, indent = 4, sort_keys = True)) # This just dumps the data into a json file
        

## To-Do:
# -> Show all trains on [T]
# -> Fix input checks on [T]
# -> Stop errors.
# -> Do error correction on [T]
# -> Choose depart and arrive [S]

print("            .-:           .:            ")
print("          .--=+=.         .==:          ")
print("        :----====-.       .=+++:        ")
print("      :===---=====--.     .=+++++-      ")
print("    :=======-====----:.   .=+++++++-    ")
print("  :=+===========-----:::  .=+++++++++-  ")
print(":++++++++++++==-----::::..:+++++++*****:")
print(" :***********: :---::::...:+++++*****+: ")
print("   :*********:   :::::....:+++++***+:   ")
print("     :*######:     .:.....:+++++*+:     ")
print("       :*####:       .... :+++++:       ")
print("         :*##:            :++=:         ")
print("           :*:            :=:           ")

print("IRONRAIL by IrishTnT |", version)
print("\t    IrishTnT.com\n\n")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# parseData is used in all subquent  ┃
# functions to do any and all parsing┃
# it can be requested to store it in ┃
# a file of certain filename, but    ┃
# this argument is optional.         ┃
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def parseData(URL, fileTitle = ""):
    parsed = []

    root = ET.parse(urllib.request.urlopen(URL)).getroot()
    if debug == 1:
        print("API returned, parsing...")
    
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
        parsed.append(temp) # Adds temp to the array.
    
    if len(fileTitle) != "":
        if debug == 1:
            print("Parse complete. Writing file with name:", fileTitle)
        with open(fileTitle + ".json", "w") as f:
            f.write(json.dumps(parsed, indent = 4, sort_keys = True)) # This just dumps the data into a json file
        
        if debug == 1:    
            print("File written!")
    else:
        if debug == 1:
            print("Parse Complete.")
    
    return parsed

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# stationSearch can be used to get the ┃
# trains originating, terminating, or  ┃
# passing through the named station.   ┃
# It ensures inputs are within the API ┃
# specifications, and returns a list if┃
# there is >1 station with that name.  ┃
#--------------------------------------┃
# If the function cannot find the named┃
# station, it will attempt to find ones┃
# with similar names, and offer them as┃
# a replacement, if it cannot, it will ┃
# state that it cannot find the input. ┃
#--------------------------------------┃
# stationSearch does not save files.   ┃
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def stationSearch():
    intx = 0
    station = []
    sName = input("Enter station name: ")
    sTime = input("Enter time range (5 - 90 mins): ")
    aSt = open("allstations.json", 'r', encoding = 'UTF-8')
    allStations = json.load(aSt)
    
    while intx == 0:
        if len(sName) < 4:
            sName = input("<Search must be 4+ letters.>\nEnter station name: ")
        
        if "." in sTime:
            sTime("<Whole numbers only>\nEnter time range (5 - 90 mins): ")
        elif sTime.isdigit() == False:
            sTime("<Enter numbers only>\nEnter time range (5 - 90 mins): ")
        elif int(sTime) < 5:
            sTime("<Range too short>\nEnter time range (5 - 90 mins): ")
        elif int(sTime) > 90:
            sTime("<Range too long>\nEnter time range (5 - 90 mins): ")
        else:
            print("Searching for...", sName + ",", sTime, "minutes in the future.")
            URL = 'https://api.irishrail.ie/realtime/realtime.asmx/getStationDataByNameXML_withNumMins?StationDesc=' + sName.replace(' ', '%20') + '&NumMins=' + sTime
            sCheckName = 'http://api.irishrail.ie/realtime/realtime.asmx/getStationsFilterXML?StationText=' + sName.replace(' ', '%20')
            break
            
    station = parseData(URL)
    nameCheck = parseData(sCheckName)
    
    # Now checks doing station checking
    if nameCheck == []:
        itwo = 0
        sCheck = []
        itertwo = iter(itemtwo for itemtwo in allStations)
        
        while itwo < len(allStations):
            sCheck = next((itertwo))
            
            # This is my magnum opus. It checks for similarity, and asks if you meant a different station.
            if fuzz.ratio(sCheck["StationDesc"], sName) > 70:
                print("<Station not found!>\nDid you mean '" + sCheck["StationDesc"] + "'?")
            itwo = itwo + 1
        stationSearch()
    elif len(nameCheck) > 1:
        print("Multiple stations with that name have been found!")
        i = -1
        iterdata = iter(item for item in nameCheck)
            
        while i < len(nameCheck):
            nameCheck = next((iterdata))
            print(nameCheck["StationDesc"])
            i = i + 1
        stationSearch()
    elif len(nameCheck) == 1:
        # Now shows the relevant data.
        train = []

        i = 0
        iterdata = iter(item for item in station)
        
        while i < len(station):
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

stationSearch()