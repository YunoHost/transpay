import socket
import requests 
import json
from core.config import _cfg, load_config


# Récupération du numéro de version
def version():
    with open('VERSION') as f:
        data = f.read()
        return data

# Concaténation du numéro de version (suppression des lettres et des points)
def cversion(num):
    data = int("".join(num[1:].split('.')))
    return data

# Vérification de mise à jour disponible en fonction des releases sur le dépôt git
def check_update():
    try:
        response = requests.get('https://gitlab.kokakiwi.net/api/v4/projects/82/repository/tags', timeout=1)
        tags = response.json()

        if _cfg("branch") == "stable":
            for tag in tags:
                if tag['message'] == 'stable':
                    checked_version = cversion(tag["name"])
                    if checked_version > cversion(version()):
                        return "update_available"
                    elif checked_version < cversion(version()):
                        return "woaw"
        elif _cfg("branch") == "unstable":
            checked_version = cversion(tags[0]["name"])
            if checked_version > cversion(version()):
                return "update_available"
    except requests.exceptions.RequestException:
        return "server_error"

    return "up_to_date"
