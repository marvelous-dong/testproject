import requests


def get_access_token(keys_dict):
    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={keys_dict["apiKey"]}&client_secret={keys_dict["secretKey"]}'
    response = requests.get(host)
    if response:
        return response.json()['access_token']

