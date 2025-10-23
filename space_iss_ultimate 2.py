'''
    https://developer.cisco.com/learning/modules/automating-webex-teams-appdev/collab-webex-calling-apis-from-python-itp/write-a-get-request-in-python/
    This program:
   - Asks the user to enter an access token or use the hard coded access token.
   - Lists the user's Webex rooms.
   - Asks the user which Webex room to monitor for "/seconds" of requests.
   - Monitors the selected Webex Team room every second for "/seconds" messages.
   - Discovers GPS coordinates of the ISS flyover using ISS API.
   - Display the geographical location using geolocation API based on the GPS coordinates.
   - Formats and sends the results back to the Webex Team room.

   The student will:
   1. Import libraries for API requests, JSON formatting, epoch time conversion, and iso3166.
   2. Complete the if statement to ask the user for the Webex access token.
   3. Provide the URL to the Webex room API.
   4. Create a loop to print the type and title of each room.
   5. Provide the URL to the Webex messages API.
   6. Provide the URL to the ISS Current Location API.
   7. Record the ISS GPS coordinates and timestamp.
   8. Convert the timestamp epoch value to a human readable date and time.
   9. Provide your Geoloaction API consumer key.
   10. Provide the URL to the Geoloaction address API.
   11. Store the location received from the Geoloaction API in a variable.
   12. Complete the code to format the response message.
   13. Complete the code to post the message to the Webex room.

   urls:
   GET    https://webexapis.com/v1/rooms           # List of rooms
   POST   https://webexapis.com/v1/rooms           # Create a room
   GET    https://webexapis.com/v1/rooms/<roomID>  # Get room details
   PUT    https://webexapis.com/v1/rooms/<roomID>  # Update a room
   DELETE https://webexapis.com/v1/rooms/<roomID>  # Delete a room
'''

import os  # operating system
import sys  # excecuting python
import subprocess  # import built-in core Python libraries to obtain downloaded libraries without using terminal / cmd
import importlib  # Import libraries using their name as a string
import json  # Import JSON formatting for sharing data
import time  # Import epoch time conversion converts epoch time to human readable time
import urllib  # Helps getting requests and other internet functions
import requests  # Import libraries for API requests

url = "https://webexapis.com/v1/rooms"

libs = {"requests": "requests", "geopy": "geopy"}  # Allows geolocation from longitude and latitude
for name, lib in libs.items():
    try:
        importlib.import_module(name)  # A for loop trying to import using the library name

    except ImportError:
        print(f"Trying to import {lib} with sys.executable -m pip install {lib}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
    # If the library is not already installed, the program will attempt to install it using python -m pip install <lib>

    finally:
        importlib.import_module(name)  # Try importing the library again

from geopy.geocoders import Nominatim  # Using Nominatim geolocation data


def getWebexToken():
    prompt = "Do you wish to use the hard-coded Webex token? (y/n) "
    token = ""  # set default value
    on_file = False  # is there a copy in a text file?
    if os.path.exists("access_token.txt"):  # has access token been saved to a file?
        mtime = os.path.getmtime("access_token.txt")  # get the date and time the file was last modified in UTC format
        last_modified = time.ctime(mtime)  # convert time to human readable
        prompt = f"Do you wish to use the saved token from {last_modified}? (y/n) (This token may have expired) "
        file = open("access_token.txt", "r")  # read it in anyway. Could be expired
        token = file.read()
        file.close()
        on_file = True

    choice = input(prompt)  # Do you want to use hard coded/ textfile / paste in new?
    if choice.lower()[0] == "n":  # ensuring valid response by only taking the first letter of the response in lower case form. If it is not y, it is no.
        token = input("Copy/Paste or type in your token, and Enter: ")
        if token[0:6] != "Bearer ":  # Token must begin with "Bearer "
            token = f"Bearer {token}"  # Automatically adds "Bearer" before the token ID if the user does not put it in themselves
            file = open("access_token.txt", "w")  # save to file for next time
            file.write(token)
            file.close()

    else:
        if not on_file:  # Uses the token that's already on the program:
            token = "NzA3ZTMyYjAtMDY5ZC00NmVkLWIzMDYtZjkxYTBmODllYTZlZTZlMWM0YzQtYWMy_P0A1_636b97a0-b0af-4297-b0e7-480dd517b3f9"

    return token


def getMessages(accessToken, roomIdToGetMessages):  # Getting messages from the selected room
    GetParameters = {"roomId": roomIdToGetMessages, "max": 1}
    r = requests.get("https://webexapis.com/v1/messages", params=GetParameters, headers={"Authorization": accessToken})
    if not r.status_code == 200:  # Get the most recent message only
        raise Exception("Incorrect reply from Webex API. Status code: {}. Text: {}".format(r.status_code, r.text))  # Error from website or server

    json_data = r.json()
    if len(json_data["items"]) == 0:
        print("No data found, adding default message")  # If no previous messages were found on that room, the default message below will be printed
        postMessage(accessToken, roomIdToGetMessages, "Welcome to ISS Tracker Room")  # No messages so add one
        print("Re-start to continue")  # re-start the program to continue
        return None

    messages = json_data["items"]
    message = messages[0]["text"]
    return message  # Retrieves previous message from the room and returns it back to the calling function


def postMessage(accessToken, room_id, message):
    httpHeaders = {'Authorization': accessToken}
    body = {'roomId': room_id, 'text': message}
    response = requests.post(url="https://webexapis.com/v1/messages", headers=httpHeaders, json=body)


# posts a message in the room such as the welcome message or the different ISS outputs

def getRooms(accessToken):
    r = requests.get(url, headers={"Authorization": accessToken})  # Sending the access token to the website to authorise getting the information
    if not r.status_code == 200:
        raise Exception("Incorrect reply from Webex API. Status code: {}. Text: {}".format(r.status_code, r.text))  # Error from website or server

    # 4. Create a loop to print the type and title of each room
    print("\nList of available rooms:\n")  # \n for new line
    rooms = r.json()["items"]
    for room in rooms:
        print(f"\t{room['title']}")  # \t Tabbing in one tab space
    print()

    return rooms


def searchRoom(rooms):
    '''
	SEARCH FOR WEBEX ROOM TO MONITOR
	- Searches for user-supplied room name.
	- If found, print "found" message, returns room
	- Else prompts for re-try. No returns None
	'''
    selectedRoom = None
    while selectedRoom is None:
        roomNameToSearch = input("Which room should be monitored for the /seconds messages? (Case sensitive!) ")

        for room in rooms:
            if (room["title"].find(roomNameToSearch) != -1):
                print(f"Found room: {room['title']}")
                print(f"Welcome to {roomNameToSearch}")
                return room

        print(f"Sorry, I didn't find any room with {roomNameToSearch} in it.")
        response = input("Try again? (y/n) ")
        if respnse.lower()[0] == "n":  # All responses automatically converted to lower case and only checks the first character. 'n' is the only response that cancels out the loop
            return None


def getLocation(lon, lat):  # Function to get the name of the place from it's latitude and longitude
    geolocator = Nominatim(user_agent="http")  # Using Nominatim as the geolocation provider
    location = geolocator.reverse(f'{lat},{lon}')  # Using longitude and langitude to get name of the place
    if location == None:  # If place not found, the ISS must be over the ocean
        return 'Ocean'
    return location.raw['address'].get('country', '')  # Gives address and country if a place is found


def getISSData():
    ''' load the current status of the ISS in real-time '''
    r = requests.get("http://api.open-notify.org/iss-now.json")
    jsonData = r.json()  # Returns location data such as location, longitude, langitude and time data
    # Extract the ISS location and time
    location = jsonData["iss_position"]
    lat = float(location['latitude'])
    lon = float(location['longitude'])
    time = jsonData["timestamp"]

    return lon, lat, time


def getSpaceXData():
    url = "https://api.spacexdata.com/v5/launches/latest"  # API URL for SpaceX to get the latest launch
    r = (requests.get(url))  # gets data from the URL

    jsonData = r.json()  # Converts the data to json format which is easier to read
    output = f"flight No: {jsonData['flight_number']}, "  # Getting flight information
    output += f"Launch pad: {jsonData['launchpad']}, "  # Getting the location it went from
    output += f"Launch Date: {jsonData['date_utc']}, "  # Getting the date it went
    output += f"Mission name: {jsonData['name']}"  # Getting the mission name

    print(output)  # Prints this information
    return output


def processData(room, accessToken):
    ''' room is working '''
    roomIdToGetMessages = room["id"]  # get Room ID
    roomTitleToGetMessages = room["title"]  # get room title
    seconds = 0  # Creating a variable called seconds to define the amount of time the program should sleep for after every request
    timepassed = 0  # Keeping track of how long the program has been running for
    message = getMessages(accessToken, roomIdToGetMessages)
    last_message = message  # stops continuous printing of same message

    while True:
        for runtime in range(6):  # print messages for only for 6 seconds
            time.sleep(1)
            timepassed = timepassed + 1
            message = getMessages(accessToken, roomIdToGetMessages)
            if message.find("/") == 0:  # Checks if a user has sent a / message with seconds in the room to define the amount of the time the program should wait before sending a message
                if (message[1:].isdigit()):  # Checks the numbers after the slash
                    seconds = int(message[1:])
                    print(f"Message received: {message} = time.sleep({seconds})")
                    # for the sake of testing, the max number of seconds is set to 5.
                    if seconds > 5:
                        print("Your requested sleep time has been reduced to 5 seconds")
                        seconds = 5
                    postMessage(accessToken, roomIdToGetMessages, (f"Message will print in {seconds} seconds"))  # Post the message to the Webex room after the requested sleep time
                    time.sleep(seconds)
                    lon, lat, timestamp = getISSData()  # Get the ISS location
                    timeString = time.ctime(timestamp)  # Converts time stamp to human readable format
                    CountryResult = getLocation(lon, lat)  # Converts location to human readable format
                    if CountryResult == "Ocean":
                        responseMessage = "On {}, the ISS was flying over a body of water at latitude {}° and longitude {}°.".format(timeString, lat, lon)  # args = arguments which tell the program which data to insert
                    else:
                        responseMessage = f"On {timeString}, the ISS was flying over {CountryResult}"
                    print(f"Sending to Webex: {responseMessage}")  # print the response message
                    postMessage(accessToken, roomIdToGetMessages, responseMessage)  # Post the message to the Webex room
                    postMessage(accessToken, roomIdToGetMessages, getSpaceXData())  # Post the message to the Webex room
                    print()  # Leave a blank line
                else:
                    print("message did not contain time in seconds")
            else:
                if message != last_message:
                    print(message)
                    last_message = message

        response = input("Do you want to continue? (y/n) ")
        if response.lower()[0] == "n":  # All responses automatically converted to lower case and only checks the first character. 'n' is the only response that cancels out the loop
            return  # stops the program


def main():
    ''' access token lasts for 12 hours from login to website so needs to be replaced frequently '''
    accessToken = getWebexToken()  # Get the token with this function
    rooms = getRooms(accessToken)  # Get list of rooms
    if rooms != None:  # check at least one room exists
        room = searchRoom(rooms)  # Allow user to search for a room
        if room != None:  # room has been found
            processData(room, accessToken)  # Work with this room

    input("\nEnter to quit")


main()

