# Data Web Server
This is a quick project to be able receive data from multiple sources (e.g. arduinos, rapsberry pies) connected on the same network and display in real time the graph of these data.



## Installation
### Requires
* Python 3.5 or higher
#### Front-End Dev
* node [installation](https://nodejs.org/en/download/) (Only needed to modify client side)
* Run ```npm install -g typescript browserify```
### Minimal
* Fill app.ini with you desired parameters
* Run ```pip install -r requirements```
### Front-End Dev
* Run ```npm install```

## Data Receiving Server
The data server accept TCP connection at the address and port defined in app.ini
The TCP Message should have the following format:
HEADER: name length (1 byte) | param type (1 byte)
BODY: name | value
For the moment, only two parameter types are supported:
* 0: int (32 bits)
* 1: float  (32 bits)

## Graph Server
The graph server will be available at the address and port defined in app.ini