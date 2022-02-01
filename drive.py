# Import modules needed.
from pydrive.auth import GoogleAuth

# Runs google authentication by launching a login screen on the web broswer. Saving it under the variable drive and
# and saves this to a text file.
def login():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive

from datetime import datetime

