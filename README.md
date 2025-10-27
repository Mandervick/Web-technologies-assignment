# 🚀 Space Bot API Investigation Sheet

**Total Marks: 30**  
**Part 1: Collect Required API Documentation**

This investigation sheet helps you gather key technical information from the three APIs required for the Space Bot project: **Webex Messaging API**, **ISS Current Location API**, and a **Geocoding API** (LocationIQ or Mapbox or other), plus the Python time module.

---

## ✅ Section 1: Webex Messaging API (7 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `https://webexapis.com/v1/` |
| Authentication Method | `Log on to Cisco Webex Developer and copy access token which lasts for 12 hours` |
| Endpoint to list rooms | `response = requests.get(url = "https://webexapis.com/v1/rooms")` |
| Endpoint to get messages | `response = requests.get(url="https://webexapis.com/v1/messages")` |
| Endpoint to send message | `response = requests.post(url="https://webexapis.com/v1/messages")` |
| Required headers | `httpHeaders = {'Authorization': accessToken}` |
| Sample full GET or POST request | `r = requests.get("https://webexapis.com/v1/rooms", headers={"Authorization": accessToken})` |

---

## 🛰️ Section 2: ISS Current Location API (3 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `http://api.open-notify.org/` |
| Endpoint for current ISS location | `r = requests.get("http://api.open-notify.org/iss-now.json")` |
| Sample response format (example JSON) |  
```
{'timestamp': 1761574483, 'iss_position': {'latitude': '-27.9157', 'longitude': '-34.1199'}, 'message': 'success'}
```
|

---

## 🗺️ Section 3: Geocoding API (LocationIQ or Mapbox or other) (6 marks)

| Criteria | Details |
|---------|---------|
| Provider used (circle one) | **LocationIQ / Mapbox/ other -provide detail** | Using geopy.geocoders (The provider used is geopy Nominatim)
| API Base URL | `This is hidden in the geopy library and is not available for external viewing` |
| Endpoint for reverse geocoding | `There is no direct Endpoint because it is encoded in the library` |
| Authentication method | `None required - Free to use` |
| Required query parameters | `geolocator = Nominatim(user_agent="http")` |
| Sample request with latitude/longitude | `location = geolocator.reverse(f'{lat},{lon}')` |
| Sample JSON response (formatted example) |  
```
Kepulauan Bangka Belitung, Sumatera, Indonesia
```
|

---

## ⏰ Section 4: Epoch to Human Time Conversion (Python time module) (2 marks)

| Criteria | Details |
|---------|---------|
| Library used | `time` |
| Function used to convert epoch | `time.ctime()` |
| Sample code to convert timestamp |  
```  
timeString = time.ctime(1761576851)
```
|
| Output (human-readable time) | `Mon Oct 27 14:54:11 2025` |

---

## 🧩 Section 5: Web Architecture & MVC Design Pattern (12 marks)

### 🌐 Web Architecture – Client-Server Model
- (Explain the communication between them & include a block diagram )

- **Client**: The communication between a server and a client follows a request given by the client which gets a response.
+---------+        Request        +---------+        Query        +-----------+
| Client  | -------------------> | Internet| ------------------->|  Server   |
|         | <------------------- |         | <-------------------|           |
+---------+       Response        +---------+       Response      +-----------+
                                                       |
                                                       v
                                                 +-----------+
                                                 | Database  |
                                                 +-----------+

- **Server**: 
The server processes the request and sends back a response to the client.

### 🔁 RESTful API Usage

- Defines the rules you must follow to communicate with other software systems.
- For example, the Webex API asks for your user access token.
- The server validates this and returns the information.

### 🧠 MVC Pattern in Space Bot with examples

| Component   | Description |
|------------|-------------|
| **Model**  | The model uses data from the ISS and the chat room Webex to provide a link between users and ISS. |
| **View**   | The user interface is a console program (CLI). |
| **Controller** | A python program written to handle user input and manipulate API calls to produce the output. |


---

### 📝 Notes

- Use official documentation for accuracy (e.g. developer.webex.com, locationiq.com or Mapbox, open-notify.org or other ISS API).
- Be prepared to explain your findings to your instructor or demo how you retrieved them using tools like Postman, Curl, or Python scripts.

---

### ✅ Total: /30