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
* In the project root, run ```python3 -m pip install -r requirements```
### Front-End Dev
* In the project root, run ```npm install```

## Run
* In the project root, run ```python3 app.py```

## Update Frontend
The front-end scripts are written in typescript and use node_modules.
Therefore, they need to be transpiled and linked together, the bundle_ts does these operations
To update the bundle.js file, run ```python3 bundle_ts.py```

## Data Receiving Server
The data server accept TCP connection at the address and port defined in app.ini
The TCP Message should have the following format:
HEADER: name length (1 byte) | param type (1 byte)
BODY: name | value
For the moment, only two parameter types are supported:
* 0: int (32 bits)
* 1: float  (32 bits)

### Examples
#### Python
The file [tests/send_value_to_data_server.py](tests/send_value_to_data_server.py) shows an example on how-to send data 
to the data server
#### C++
The file [tests/send_value_to_data_server.cpp](tests/send_value_to_data_server.cpp) shows an example on how-to send data 
to the data server

## Graph Server
The graph server will be available at the address and port defined in app.ini
