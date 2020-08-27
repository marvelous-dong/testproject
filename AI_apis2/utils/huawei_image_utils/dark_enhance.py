# -*- coding:utf-8 -*-

import sys
import json
from utils.huawei_image_utils import ais
from utils.huawei_image_utils import utils
from utils.huawei_image_utils import signer

#
# access image dark enhance,post data by token
#
def dark_enhance(token, image, brightness=0.9):
    endpoint = utils.get_endpoint(ais.AisService.IMAGE_SERVICE)
    _url = 'https://%s%s' % (endpoint, ais.ImageURI.DARK_ENHANCE)

    if sys.version_info.major >= 3:
        if image:
            image = image.decode("utf-8")

    _data = {
        "image": image,
        "brightness": brightness
    }

    status_code, resp = utils.request_token(_url, _data, token)
    return resp.decode('utf-8')
#
# access image dark enhance by ak,sk
#
def dark_enhance_aksk(_ak, _sk, image, brightness=0.9):
    endpoint = utils.get_endpoint(ais.AisService.IMAGE_SERVICE)
    _url = 'https://%s%s' % (endpoint, ais.ImageURI.DARK_ENHANCE)

    sig = signer.Signer()
    sig.AppKey = _ak
    sig.AppSecret = _sk

    if image:
        image = image.decode("utf-8")

    _data = {
        "image": image,
        "brightness": brightness
    }

    kreq = signer.HttpRequest()
    kreq.scheme = "https"
    kreq.host = endpoint
    kreq.uri = "/v1.0/vision/dark-enhance"
    kreq.method = "POST"
    kreq.headers = {"Content-Type": "application/json"}
    kreq.body = json.dumps(_data)

    status_code, resp = utils.request_aksk(sig, kreq, _url)
    return resp.decode('utf-8')
