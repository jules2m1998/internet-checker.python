# internet-checker.python
Version: 0.1.0

## What is it?
Tool to check the connection status of a terminal and notify the user with sounds and via a telegram bot

## How to use it?
### Install Package
``pip install requirements.txt``
### ENV variables
* Create a file named ``.env`` in the root directory of the project
* Add the following lines:
```
API_KEY = // api key of the telegram bot *required
CONN_TENTATIVE = // Number of connection terminals required
DELAY = // Delay between each connection
CHAT_ID = // Your chat id *required
```
* Run main file
```
python3 main.py
```

### Enjoy !