'''
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
'''

#Import libraries for API requests
#Import JSON formatting for sharing data
#Import epoch time conversion converts epoch time to human readable time
#Import iso3166 to convert a country code to human readable country code
import os #operating system
import sys #excecuting python
import subprocess #import built-in core Pytom libraries to obtain downloaded libraries without using terminal / cmd
import importlib #Import libraries as a string
import json
from datetime import datetime

libs = {"requests": "requests", "iso3166":"iso3166", "webexpythonsdk":"webexpythonsdk", "iss-tracker":"iss-location-tracker", "mapbox":"mapbox"}
'''
libs-Dictionary of libraries
requests-Make a request to a web page and print the response
iso3166-Convert a country code to a human readable country code
webexpythonsdk-Interact with webex using python commands
iss tracker-Gives precise location data and the number of astronauts
mapbox-Allows the program to put the iss tracker data on a map
'''

for name, lib in libs.items():
	try:
		module = importlib.import_module(name) # A for loop trying to import using the library name
		
	except ImportError:
		print(f"Trying to import {lib} with sys.executable -m pip install {lib}...") 
		subprocess.check_call([sys.executable, "-m", "pip", "install",  lib])
		# If the library is not already installed, the program will attempt to install it using python -m pip install <lib>
		
	finally:
		try:
			module = importlib.import_module(name) #Try importing the library again
		except:
			print("There was an error while importing the library") #Otherwise error message

def get_webex_token():
	token = ""
	choice = input("Do you wish to use the hard-coded Webex token? (y/n) ")#Do you want to input your own token or use what's already on the program?
	if choice.lower()[0] == "y": #ensuring valid response by only taking the first letter of the response in lower case form. If it is not y, it is no.
		token = input("Copy/Paste or type in your token, and Enter")
		if token[0:6] != "Bearer ":
			token = f"Bearer {token}" #Automatically adds "Bearer" before the token ID if the user does not put it in themselves
	else: #Uses the token that's already on the program
		token = "YmE4YTNmNWMtY2ZlNS00NDMyLWIwZGMtOTAyNjEyY2U5MGQzYzliNzFmNDQtOGRi_PE93_74f575ad-38da-4d7d-aa86-0a3f07cc90cd"
		#org.id = 636b97a0-b0af-4297-b0e7-480dd517b3f9
		# bot access token Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OLzk1NWY4ZGI3LTNiZWEtNGM1Mi05Yjc5LWMzZmViYjU4NzNhMg
	return token

def main():
	accessToken = get_webex_token()#Get the token from above
	r = requests.get("<!!!REPLACEME with URL!!!>",
					headers = {"Authorization": accessToken} #Sending the access token to the website to authorise getting the information
					)	


main()
	
