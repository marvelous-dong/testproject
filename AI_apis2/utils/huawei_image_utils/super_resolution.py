# -*- coding:utf-8 -*-

import sys
import json
from utils.huawei_image_utils import ais
from utils.huawei_image_utils import utils
from utils.huawei_image_utils import signer


# access image super resolution,post data by token

def super_resolution(token, image, scale=3, model="ESPCN"):
    endpoint = utils.get_endpoint(ais.AisService.IMAGE_SERVICE)
    _url = 'https://%s%s' % (endpoint, ais.ImageURI.SUPER_RESOLUTION)

    if image:
        image = image.decode("utf-8")

    _data = {
        "image": image,
        "scale": scale,
        "model": model
    }

    status_code, resp = utils.request_token(_url, _data, token)
    return resp.decode('utf-8')


# access image super resolution enhance,post data by sk,sk

def super_resolution_aksk(_ak, _sk, image, scale=3, model="ESPCN"):
    endpoint = utils.get_endpoint(ais.AisService.IMAGE_SERVICE)
    _url = 'https://%s%s' % (endpoint, ais.ImageURI.SUPER_RESOLUTION)

    sig = signer.Signer()
    sig.AppKey = _ak
    sig.AppSecret = _sk

    if image:
        image = image.decode("utf-8")

    _data = {
        "image": image,
        "scale": scale,
        "model": model
    }

    kreq = signer.HttpRequest()
    kreq.scheme = "https"
    kreq.host = endpoint
    kreq.uri = "/v1.0/vision/super-resolution"
    kreq.method = "POST"
    kreq.headers = {"Content-Type": "application/json"}
    kreq.body = json.dumps(_data)

    status_code, resp = utils.request_aksk(sig, kreq, _url)
    return resp.decode('utf-8')

