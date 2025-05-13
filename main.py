import os
import eel
from engine.features import *
from engine.command import *

def start():
    eel.init("www") #point to the directory where our front end is

    platAssistantSound()

    # os.system('open -a "Safari" "http://localhost:8000/index.html"')
    os.system('open -a "Google Chrome" "http://localhost:8000/index.html"')

    eel.start("index.html", mode=None , host="localhost", block=True)