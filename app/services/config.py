import configparser
import os
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
