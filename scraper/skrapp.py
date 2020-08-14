import os
import requests
import configparser

path_current_directory = os.path.dirname(__file__)
path_config_skrapp_file = os.path.join(path_current_directory, '../config', 'skrapp.ini')

config = configparser.ConfigParser()
config.read(path_config_skrapp_file)

SKRAPP_URL = "https://api.skrapp.io/api/v2/find?firstName={}&lastName={}&domain={}"
skrapp_api_key = config['API']['api_key']

headers = {"X-Access-Key": skrapp_api_key, "Content-Type": "application/json"}
session = requests.session()


def retrieve_email(name, domain):
    first_name = name.split()[0]; last_name = name.split()[-1]
    domain = domain.split('@')[-1]

    try:
        url = SKRAPP_URL.format(first_name, last_name, domain)
        response = session.get(url, headers=headers).json()
        if response['accuracy'] < 50:
            raise Exception
        return response['email']
    except:
        return None