import socket
import requests 
import json
from core.config import _cfg, load_config

branch = "stable"
#branch = "unstable"


def version():
    with open('VERSION') as f:
        data = f.read()
        return data

def check_update():
    try:
        response = requests.get('https://gitlab.kokakiwi.net/api/v4/projects/82/repository/tags', timeout=1)
        tags = response.json()

        if _cfg("branch") == "stable":
            for tag in tags:
                if tag['message'] == 'stable':
                    if tag["name"] != version():
                        return False
        elif _cfg("branch") == "unstable":
            if tags[0]["name"] != version():
                return False
    except requests.exceptions.RequestException:
        print("Could not check the gitlab repo :c")

    return True
