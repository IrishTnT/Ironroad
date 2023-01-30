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

version = "v0.3 BETA"

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
    
    # This check all stations with that name. This only
    if onListLock == 0:
        nameCheck = parseData(sCheckName)
   
# Initialising, %2%     
def init():
    allStations = parseData("http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML")
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