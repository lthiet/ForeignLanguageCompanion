import configparser
import os
import requests
cfg = configparser.ConfigParser()
cfg.read(os.path.join(os.getcwd(), 'config.ini'))


def get_header(service):
    key = cfg[service]['key']
    location = cfg[service]['location']
    return {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
    }


def get_token():
    fetch_token_url = cfg['speech']['endpoint']
    headers = {
        'Ocp-Apim-Subscription-Key': cfg['speech']['key']
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = str(response.text)
    return access_token
