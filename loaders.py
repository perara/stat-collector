import os
import json
import time
PATH = os.path.dirname(os.path.abspath(__file__))

def load_tick():
    # Load Tick
    with open(os.path.join(PATH, ".tick"),'r') as f:
        try:
            tick = int(f.read())
        except:
            tick = 0

    return tick


def save_tick(tick):
    # Load Tick
    with open(os.path.join(PATH, ".tick"),'w') as f:
        f.write(str(int(tick))) # Validate that its a int and write as string


def load_config():

    # Load configuration
    with open(os.path.join(PATH, "./config.json")) as data_file:
        config = json.load(data_file)
    return config