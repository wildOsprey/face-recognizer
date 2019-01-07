# Description
Face recognition app using PyQt5 and dlib.

## Requirements
For running this project you will need following:
1. Python 3 environment
2. MongoDB Server(https://www.mongodb.com/download-center/community)
3. Required packages
4. Webcam

## Preparation

Required Python version - 3.6 and higher
All required packages should be installed running ```pip install -r requirements.txt```

## Runing

```python main.py```

## Setup server
1. Create folder with db data (ex. D://data//people)
2. Go to C:\Program Files\MongoDB\Server\4.0\bin
3. Run cmd from this folder
4. ``` ./mongod --port 27017 --dbpath D://data//people``` (if it can't find mongod command try ``` mongod --port 27017 --dbpath D://data//people```
