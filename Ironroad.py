from pathlib import Path
from thefuzz import fuzz
from thefuzz import process
import json
import xml.etree.ElementTree as ET
import urllib
import urllib.request

# BETA BRANCH CODE.

# The structure of:
#   Function Declaration - %1%
#   Pre-initialising     - %2%
#   Initialising         - %3%
#   main                 - %4%
# is used here under advice.
# CTRL + F phrases are provided for each section.

version = "v0.3.1 BETA"

# Function Declaration, %1%

# parseData() is used by all subsequent functions.
# It is used to directly query the Irish Rail API,
# parse the data from XML to JSON, and then return
# the data as a JSON object. To call this function,
# pass the URL of the API as a string, and you may
# also pass a filename, which if filled will save
# the data as a file on disk.
def parseData(URL, fileTitle = ""):
    parsed = []

    # Thanks to Saetom for the genius work of this parsing.
    root = ET.parse(urllib.request.urlopen(URL)).getroot()
    
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
    if len(fileTitle) != 0:
        with open(fileTitle + ".json", "w") as f:
            f.write(json.dumps(parsed, indent = 4, sort_keys = True)) # This just dumps the data into a json file
    
    return parsed

# errorBroker() is used to handle errors. It takes
# two arguments, the error code, and if it should
# print the error to the console. It will always
# return a string with the error code and the
# error message. It will also print the error to
# the console if the second argument is True.
def errorBroker(errorData, toPrint):
    if errorData == 0:
        if toPrint:
            print(errorData)
            
        return errorData

# stationSearch() returns all trains originating,
# terminating, or passing through any station.
# It takes three arguments, the station name,
# the time to search for, and if it should print
# the data to the console.
# The station name must be 4+ characters long.
# The time must be between 5 and 90 minutes.
# The function will return an array or a string.
# The function will return an array with the
# data on a successful function call.
# The function will return a string with the
# error code and the error message on an
# unsuccessful function call. This is handled
# by errorBroker().
def stationSearch(stationName = "", timeSearch = 0, printData = True):
    allStations = parseData("http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML")
    intx = 0
    onListLock = 0
    sCheckName = ""
    nameCheck = ""
    station = []
    
    # Error checking
    if len(stationName) < 4:
        return errorBroker("ERROR! Station name less than 4 characters!", printData)
    elif type(stationName) != str:
        return errorBroker("ERROR! stationName must be a string!", printData)
    elif timeSearch < 5 or timeSearch > 90:
        return errorBroker("ERROR! Time search less than 5 or greater than 90 minutes!", printData)
    elif type(printData) != bool:
        return errorBroker("ERROR! printData must be True or False!", printData)
    elif type(timeSearch) != int:
        return errorBroker("ERROR! timeSearch must be an integer!", printData)
    elif "." in timeSearch:
        return errorBroker("ERROR! timeSearch must be a whole number!", printData)
    
    # Handling edge-cases in the API and building the URL for the request.
    if "Hazelhatch" in stationName or "Celbridge" in stationName:
        onListLock = 1 # Locking the main station checking.
        URL = 'http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByCodeXML_WithNumMins?StationCode=HZLCH&NumMins=' + timeSearch
        
        if printData:
            print("Searching for... Hazelhatch and Celbridge,", timeSearch, "minutes in the future.")
    elif "Park West" in stationName or "Cherry Orchard" in stationName:
        onListLock = 1 # Locking the main station checking.
        URL = 'http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByCodeXML_WithNumMins?StationCode=CHORC&NumMins=' + timeSearch
        
        if printData:
            print("Searching for... Park West and Cherry Orchard,", timeSearch, "minutes in the future.")
    elif "Clondalkin" in stationName or "Fonthill" in stationName:
        onListLock = 1 # Locking the main station checking.
        URL = 'http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByCodeXML_WithNumMins?StationCode=CLDKN&NumMins=' + timeSearch
        
        if printData:
            print("Searching for... Clondalkin and Fonthill,", timeSearch, "minutes in the future.")
    elif "Adamstown" in stationName:
        onListLock = 1 # Locking the main station checking.
        URL = 'http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByCodeXML_WithNumMins?StationCode=ADMTN&NumMins=' + timeSearch
        
        if printData:
            print("Searching for... Adamstown,", timeSearch, "minutes in the future.")
    elif "Little" in stationName or "Island" in stationName or "LittleIsland" in stationName:
        onListLock = 1 # Locking the main station checking.
        URL = 'http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByCodeXML_WithNumMins?StationCode=LSLND&NumMins=' + timeSearch
        
        if printData:
            print("Searching for... Little Island,", timeSearch, "minutes in the future.")
    else:
        onListLock = 0
        URL = 'https://api.irishrail.ie/realtime/realtime.asmx/getStationDataByNameXML_withNumMins?StationDesc=' + stationName.replace(' ', '%20') + '&NumMins=' + timeSearch
        sCheckName = 'http://api.irishrail.ie/realtime/realtime.asmx/getStationsFilterXML?StationText=' + stationName.replace(' ', '%20')
        
        if printData:
            print("Searching for...", stationName + ",", timeSearch, "minutes in the future.")
    
    # This checks the station name you gave it. It will return an empty list if it doesn't exist.
    station = parseData(URL)
    
    # This check all stations with that name. This only runs if it isn't an edge-case.
    if onListLock == 0:
        nameCheck = parseData(sCheckName) # Getting the trains passing through the station, this will be empty if the station does not exist.
        
        if nameCheck == []:
            itwo = 0
            sCheck = []
            sFound = 0
            selfLock = 0
            itertwo = iter(itemtwo for itemtwo in allStations)
            
            while itwo < len(allStations):
                sCheck = next((itertwo))
                
                # This is my magnum opus. It checks for similarity, and asks if you meant a different station.
                # Some stations in the API have multiple entries, this must be handled in this wonky way.
                # If it wasn't handled here, if you mistyped it, it'd show the station multiple times.
                # sFound stops the function from incorrectly stating that the station does not exist if it is found.
                # selfLock stops edge-case stations from printing the same message multiple times.
                if fuzz.ratio("Hazehatch", stationName) >= 70 or fuzz.ratio("Celbridge", stationName) >= 70 or fuzz.ratio("Hazehatch and Celbridge", stationName) >= 70:
                    if sCheck["StationDesc"] == "Hazelhatch" and selfLock == 0:
                        return errorBroker("<Station not found!>\nDid you mean 'Hazelhatch'?", printData)
                        sFound = 1
                        selfLock = 1
                elif fuzz.ratio("Park West", stationName) >= 70 or fuzz.ratio("Cherry Orchard", stationName) >= 70 or fuzz.ratio("Park West and Cherry Orchard", stationName) >= 70:
                    if sCheck["StationDesc"].lower() == "park west" and selfLock == 0:
                        return errorBroker("<Station not found!>\nDid you mean 'Park West and Cherry Orchard'?", printData)
                        sFound = 1
                        selfLock = 1
                elif fuzz.ratio("Clondalkin", stationName) >= 70 or fuzz.ratio("Fonthill", stationName) >= 70 or fuzz.ratio("Clondalkin and Fonthill", stationName) >= 70:
                    if sCheck["StationDesc"].lower() == "park west" and selfLock == 0:
                        return errorBroker("<Station not found!>\nDid you mean 'Clondalkin'?", printData)
                        sFound = 1
                        selfLock = 1
                elif fuzz.ratio("Adamstown", stationName) >= 70:
                    if sCheck["StationDesc"].lower() == "adamstown" and selfLock == 0:
                        return errorBroker("<Station not found!>\nDid you mean 'Adamstown'?", printData)
                        sFound = 1
                        selfLock = 1
                elif fuzz.ratio(sCheck["StationDesc"], stationName) >= 70:
                    errorMsg = errorMsg + "<Station not found!>\nDid you mean '" + sCheck["StationDesc"] + "'?\n"
                    return errorBroker(errorMsg, printData)
                    sFound = 1
                itwo += 1
                
            if sFound == 0:
                errorBroker("ERROR! A station with that name cannot be found.", printData)
            
        elif len(nameCheck) > 1:
            errorMsg = "Multiple stations with that name have been found!\n"
            i = -1
            iterdata = iter(item for item in nameCheck)
                
            while i < len(nameCheck):
                nameCheck = next((iterdata))
                errorMsg = errorMsg + nameCheck["Destination"] + "/n"
                i += 1
            
            return errorBroker(errorMsg, printData)

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
                    print("Train from", train["Origin"], "to", train["Destination"], intype, train["Duein"], "minutes.", str(runningtype))
                else:
                    print("Train from", train["Origin"], "to", train["Destination"], intype, train["Duein"], "minute.", str(runningtype))
                    
                i += 1
            
            if len(station) == 0:
                print("No trains in found in that time frame.")
                stationSearch()
            
    # This only runs when an edge-case station is entered.
    else:
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
                # Putting together the early phrase, it's an absolute as the API reports earliness
                # as a minus number.
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
                print("Train from", train["Origin"], "to", train["Destination"], intype, train["Duein"], "minutes.", str(runningtype))
            else:
                print("Train from", train["Origin"], "to", train["Destination"], intype, train["Duein"], "minute.", str(runningtype))
                
            i += 1
        
        if len(station) == 0:
            print("No trains in found in that time frame.")
            stationSearch()
   
# Initialising, %2%     
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


# Main, %3% 
if __name__ == "__main__":
    init()
    
    stationSearch()