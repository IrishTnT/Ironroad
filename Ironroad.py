from pathlib import Path
from thefuzz import fuzz
from thefuzz import process
import json
import xml.etree.ElementTree as ET
import urllib
import urllib.request
import logging

# BETA BRANCH CODE.

# The structure of:
#   Function Declaration - %1%
#   Pre-initialising     - %2%
#   Initialising         - %3%
#   main                 - %4%
# is used here under advice.
# CTRL + F phrases are provided for each section.

debug = 0 # This will show extra information on what the code is doing, turn to 0 for a more User-friendly console experience.
version = "v0.2.4"

## To-Do:
# -> Show all trains on [T]
# -> Write T [T]
# -> Stop errors.
# -> Do error correction on [T]
# -> Choose depart and arrive [S]

# Functions are declared here! %1%

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# parseData is used in all subquent  ┃
# functions to do any and all parsing┃
# it can be requested to store it in ┃
# a file of certain filename, but    ┃
# this argument is optional.         ┃
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def parseData(URL, fileTitle = ""):
    parsed = []

    # Thanks to Saetom for the genius work of this parsing.
    root = ET.parse(urllib.request.urlopen(URL)).getroot()
    if debug == 1:
        print("[DEBUG] API returned, parsing...")
    
    for child in root:
        # Loops through all child elements of the XML root.
        temp = {}
        # Creating an empty object each time the loop runs.
        for data in child:
            # Loops through all the child elements in each element.
            # data.tag returns the name of the tag.
            # Tags appear with the URL included, splitting the string into an array at '}'.
            temp[data.tag.split("}")[1]] = data.text
            # Since all (good) languages index from '0', this selects the name part of "['{url}', 'name']" and makes it
            # a key in temp with the name of the tag, and its value.
        parsed.append(temp) # Adding temp to the array.
    
    # File writing is an optional extra and will only write a file if a filename is given.
    if len(fileTitle) != "":
        if debug == 1:
            print("[DEBUG] Parse complete. Writing file with name:", fileTitle)
        with open(fileTitle + ".json", "w") as f:
            f.write(json.dumps(parsed, indent = 4, sort_keys = True)) # This just dumps the data into a json file
        
        if debug == 1:    
            print("[DEBUG] File written!")
    else:
        if debug == 1:
            print("[DEBUG] Parse Complete.")
    
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
# stationSearch also does not accept   ┃
# arguments when called just yet, all  ┃
# variable gathering is done internally┃
#--------------------------------------┃
# All data input is handled internally ┃
# and this function cannot handle      ┃
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def stationSearch():
    intx = 0
    station = []
    sName = input("Enter station name: ")
    sTime = input("Enter time range (5 - 90 mins): ")
    aSt = open("allstations.json", 'r', encoding = 'UTF-8')
    # This allows my magnum opus to actually work.
    # When loading a JSON file from disk, ALWAYS do a json.load()
    allStations = json.load(aSt)
    
    # Data input, stuck in an infinite loop so you can re-enter correct data
    # if you fail the original input checking.
    while intx == 0:
        if len(sName) < 4:
            sName = input("<Search must be 4+ letters.>\nEnter station name: ")
        
        if "." in sTime:
            sTime = input("<Whole numbers only>\nEnter time range (5 - 90 mins): ")
        elif sTime.isdigit() == False:
            sTime = input("<Enter numbers only>\nEnter time range (5 - 90 mins): ")
        elif int(sTime) < 5:
            sTime = input("<Range too short>\nEnter time range (5 - 90 mins): ")
        elif int(sTime) > 90:
            sTime = input("<Range too long>\nEnter time range (5 - 90 mins): ")
        else:
            print("Searching for...", sName + ",", sTime, "minutes in the future.")
            URL = 'https://api.irishrail.ie/realtime/realtime.asmx/getStationDataByNameXML_withNumMins?StationDesc=' + sName.replace(' ', '%20') + '&NumMins=' + sTime
            sCheckName = 'http://api.irishrail.ie/realtime/realtime.asmx/getStationsFilterXML?StationText=' + sName.replace(' ', '%20')
            break
     
    # There is most likely an improved implementation that can be done here.
    # station calls the API to get trains, nameCheck calls a different part
    # of the API to see if the station even exists.
    station = parseData(URL)
    nameCheck = parseData(sCheckName)
    
    # Completing station checking now.
    if nameCheck == []:
        itwo = 0
        sCheck = []
        sFound = 0
        itertwo = iter(itemtwo for itemtwo in allStations)
        
        while itwo < len(allStations):
            sCheck = next((itertwo))
            
            # This is my magnum opus. It checks for similarity, and asks if you meant a different station.
            if fuzz.ratio(sCheck["StationDesc"], sName) >= 70:
                print("<Station not found!>\nDid you mean '" + sCheck["StationDesc"] + "'?")
                sFound = 1 # Stops the function incorrectly reporting that station doesn't exist.
            itwo += 1
        
        # Should the function not find anything, it says this.
        if sFound == 0:
            print("Station cannot be found. Please try again.")
            
        # Recursive function calling to keep function short.
        stationSearch()
    elif len(nameCheck) > 1:
        print("Multiple stations with that name have been found!")
        i = -1
        iterdata = iter(item for item in nameCheck)
            
        while i < len(nameCheck):
            nameCheck = next((iterdata))
            print(nameCheck["StationDesc"])
            i += 1
        
        # Recursive call.
        stationSearch()
    elif len(nameCheck) == 1:
        # Since there is exactly one result, create array called train which holds all of the train data..
        train = []

        i = 0
        iterdata = iter(item for item in station)
        
        # Iterating through all the trains found at that station and put into train.
        while i < len(station):
            train = next((iterdata))
            
            # Arriving / Departing and Early/Late/On-Time is done here to keep code modular and to shorten printing.
            if train["Locationtype"].lower() == "s" or train["Locationtype"].lower() == "d":
                intype = "arriving in"
            elif train["Locationtype"].lower() == "o":
                intype = "departing in"
                
            if int(train["Late"]) < -1:
                ## Putting together the early phrase, it's an absolute as the API reports earliness
                ## as a minus number.
                time_early = str(abs(int(train["Late"])))
                runningtype = "".join(("Running ", time_early, " minutes early."))
            elif int(train["Late"]) == -1:
                time_early = str(abs(int(train["Late"])))
                runningtype = "".join(("Running ", time_early, " minute early."))
            elif int(train["Late"]) == 0:
                runningtype = "Running on time."
            elif int(train["Late"]) == 1:
                runningtype = "".join(("Running ", train["Late"], " minute late."))
            elif int(train["Late"]) > 1:
                runningtype = "".join(("Running ", train["Late"], " minutes late."))
            
            if int(train["Duein"]) != 1:
                print("Train from", train["Origin"], "to", train["Direction"], intype, train["Duein"], "minutes.", str(runningtype))
            else:
                print("Train from", train["Origin"], "to", train["Direction"], intype, train["Duein"], "minute.", str(runningtype))
                
            i += 1

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# trainSeach can be used to find all   ┃
# trains currently going to the set    ┃
# destination, or starting in the      ┃
# next 10 minutes.                     ┃
# Interestingly, Irish Rail has this   ┃
# weird thing:                         ┃
# "Direction is either Northbound or   ┃
# Southbound for trains between Dundalk┃
# and Rosslare and between Sligo and   ┃
# Dublin."                             ┃
# I don't really know why they do this,┃
# but they do, and this handles it.    ┃
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def trainSearch():
    allTrains = []
    chosenTrains = []
    itrains = 0
    URL = ""
    aTrainsURL = "http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML_WithTrainType?TrainType=A"
    
    tChoice = input("Please select your choice of train:\n(M)ainline\n(D)ART\n(S)uburban\n(A)ll Trains\n")
    
    # Doing Choice Parsing
    if tChoice.lower() == "m" or tChoice.lower() == "mainline":
        print("Selected Mainline trains.")
        URL = "http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML_WithTrainType?TrainType=M"
    elif tChoice.lower() == "d" or tChoice.lower() == "dart":
        print("Selected DART trains.")
        URL = "http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML_WithTrainType?TrainType=D"
    elif tChoice.lower() == "s" or tChoice.lower() == "suburban":
        print("Selected Suburban trains.")
        URL = "http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML_WithTrainType?TrainType=S"
    elif tChoice.lower() == "a" or tChoice.lower() == "all" or tChoice.lower() == "all trains":
        print("Selected all trains.")
        URL = "http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML_WithTrainType?TrainType=A"
    else:
        print("Improper choice entered, please try again.")
        
        # Recurisve call.
        trainSearch()

    # There is most likely an improved implementation that can be done here.
    # chosenTrains calls the API to get trains of that line, allTrains calls
    # all trains to see if the destination they are about to search is on
    # another line.
    chosenTrains = parseData(URL)
    
    tDest = input("Enter your destination: ")
    
    # Lock exists to prevent the 'No trains found' code from executing if trains were, actually, found.
    Lock = 0
    
    # Doing some input fixing.
    if "to " not in tDest.lower():
        
        tDest = "to " + tDest

    # Resolving (issuse #12) where len(chosenTrains) reports the length of all
    # the sub-elements within the main table, which is always 7.
    # This is fixed by setting the while limit variable before we run the loop.
    ctLength = len(chosenTrains)
    
    # Now showing all the locations of that destination.
    iterdata = iter(item for item in chosenTrains)
    while itrains < ctLength:
        chosenTrains = next((iterdata))

        if chosenTrains["Direction"].lower() == tDest.lower():
            # 'No trains found' will not execute.
            Lock = 1

            # Relevant information is stored in <PublicMessage> which I need to parse.
            pmRaw = chosenTrains["PublicMessage"].replace('\\n', '\n').splitlines()
            
            # To make the returned print more legible at first-glance, I must
            # reconstruct pmRaw into pmData with some tom-foolery.
            # Since some data is in different places depending on TrainStatus,
            # that must be accounted for here.
            
            if chosenTrains["TrainStatus"].lower() == "n":
                # I hate this. I REALLY hate this, but it has to happen.
                # This gets the Departure time of the not-yet-departed train
                # and places it in the pmData array where it will exist if
                # it had departed.
                tDepTime = (pmRaw[-1].split())[-1]

                # Getting tpDest.
                tpDest = (pmRaw[1].split(' to '))[1]

                # pmData structure for a scheduled train is as follows:
                # 0 = Train Code
                # 2 = Route Name
                # 3 = Expected Departure Time
                pmData = [pmRaw[0], tpDest, pmRaw[1], tDepTime]
                
                print("The next train to", tpDest, "is the", pmData[2], "train. Expected departure", pmData[3])
            elif chosenTrains["TrainStatus"].lower() == "r":
                # It gets worse this time. So much worse.
                pmBod = pmRaw[1].split()
                tDepTime = pmBod[0]

                # There are multi-word stations in the network, up to
                # five words long, including special characters. The
                # parsing of the Origin and Destination stops must be
                # capable of handling that. This does that.
                routeRaw = pmRaw[1].replace(tDepTime + ' - ', '').partition(' (')
                routeParse = routeRaw[0].split(' to ')

                # Now grabbing the Off-Schedule Time
                ostRaw = pmRaw[1].split('(')
                offScheduledTime = (ostRaw[1].split())[0]

                # Setting Off-Schedule Phrase based on the OST
                # I know this looks bad, but I need to do it this way. I've done it in stationSearch, too.
                if int(offScheduledTime) < -1:
                    offSchedulePhrase = str(abs(int(offScheduledTime))) + " minutes early."
                elif int(offScheduledTime) == -1:
                    offSchedulePhrase = str(abs(int(offScheduledTime))) + " minute early."
                elif int(offScheduledTime) == 0:
                    offSchedulePhrase = "on schedule."
                elif int(offScheduledTime) == 1:
                    offSchedulePhrase = str(abs(int(offScheduledTime))) + " minute late."
                elif int(offScheduledTime) > 1:
                    offSchedulePhrase = str(abs(int(offScheduledTime))) + " minutes late."

                # Finally, grabbing the stop data.
                stopData = pmRaw[2].replace('Departed ', '').replace('Arrived ', '').split(' next stop ')
                
                # pmData structure for a running train is as follows:
                # 0 = Train Code
                # 1 = Departure Time
                # 2 = Origin
                # 3 = Destinatiom
                # 4 = Off-Schedule Time
                # 5 = Previous Stop
                # 6 = Next Stop
                pmData = [pmRaw[0], tDepTime, routeParse[0], routeParse[1], offSchedulePhrase, stopData[0], stopData[1]]

                print("The next train to", pmData[3], "is the", pmData[1], "train from", pmData[2], "currently between", pmData[5], "and", pmData[6] + ". Running", pmData[4])
            
        itrains += 1

    if Lock == 0:
        print("\nSTATION NOT FOUND! PLEASE TRY AGAIN!\n")
        trainSearch()

# In pre-initialising, the current list of stations must be gathered for comparison. %2%
def pre_init():
    aSP = Path("./allstations.json")
    if aSP.is_file():
        if debug == 1:
            print("[DEBUG] allstations.json exists")
    else:
        if debug == 1:
            print("[DEBUG] allstations.json doesn't exist. Grabbing.")
            
        parseData("http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML", "allstations")
        
        if debug == 1:
            print("[DEBUG] Parse complete. Writing allstations.json")

# Initialising creates the splash. %3%
def init():
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
    
# Body of code %4%
if __name__ == "__main__":
    pre_init()
    
    init()
    
    choice = ""
    
    choice = input("Please choose which you want to do:\n1. stationSearch()\n2. trainSearch()\n")
    
    if int(choice) == 1:
        stationSearch()
    elif int(choice) == 2:
        trainSearch()
    else:
        print("Improper choice.")
