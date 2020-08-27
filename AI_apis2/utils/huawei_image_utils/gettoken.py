import json
from utils.huawei_image_utils import ais
from utils.huawei_image_utils import utils
from urllib import request


def get_response(_url, auth_data):
    _headers = {
        'Content-Type': 'application/json'
    }

    data = json.dumps(auth_data).encode('utf8')
    req = request.Request(_url, data, _headers)
    return request.urlopen(req)


def get_token(username, password, domain):
    region_name = utils.get_region()

    auth_data = {
        "auth": {
            "identity": {
                "password": {
                    "user": {
                        "name": username,
                        "password": password,
                        "domain": {
                            "name": domain
                        }
                    }
                },
                "methods": [
                    "password"
                ]
            },
            "scope": {
                "project": {
                    "name": region_name
                }
            }
        }
    }

    _url = 'https://%s/v3/auth/tokens' % ais.AisEndpoint.IAM_ENPOINT

    resp = get_response(_url, auth_data)
    X_TOKEN = resp.headers['X-Subject-Token']
    return X_TOKEN



