import requests
import os

FACE_DETECTION_KEYS = {
    "APP_ID": "21288257",
    "API_Key": "7FCo8BLD2MX7HpULiRs4NiAL",
    "Secret_Key": "3ZlyV3nSTMaoc2ZHoXCmQjPzILCPGr7E"
}

IMAGE_RECOGNIZATION_KEYS = {
    "APP_ID": "21315824",
    "API_Key": "xqMo1lkf90gb7uTX43hEO2pM",
    "Secret_Key": "jGbG1w6ANEyZwQGGxSmS0slVTdYdSOxs"

}

IMAGE_DIR = os.path.join(os.path.dirname(__file__), "test_imgs")
SAVING_DIR = os.path.join(os.path.dirname(__file__), "show_tests")


def get_access_token(keys_dict):
    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={keys_dict["API_Key"]}&client_secret={keys_dict["Secret_Key"]}'
    response = requests.get(host)
    if response:
        return response.json()['access_token']

