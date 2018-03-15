
# gcal_fan (Google Calendar controlling IR Cooling Fan)
Scheduling and controlling cooling fan via remote IR and Google Calendar

# Software Requirements
* Python control for Broadlink RM2 IR controllers
	https://github.com/jazzina/python-broadlink
* python > 2.6
* pip

# Hardware Requirements
* Broadlink Universal WIFI / IR Remote
* An IR controlled cooling fan

# Install required packages

> `sudo pip install -r requirements.txt`

Or in case you are through a proxy

> `sudo pip install -r requirements.txt --proxy $PROXY`

# Configuring Google Calendar access

## Service account private key files
A service account private key file can be used to obtain credentials for a service account. 
You can create a private key using the Credentials page of the Google Cloud Console.

For further information refer to: https://google-auth.readthedocs.io/en/latest/user-guide.html

