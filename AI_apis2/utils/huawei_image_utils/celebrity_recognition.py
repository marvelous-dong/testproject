# -*- coding:utf-8 -*-

import sys
import json
from utils.huawei_image_utils import ais
from utils.huawei_image_utils import utils
from utils.huawei_image_utils import signer


#
# access image tagging
#
def celebrity_recognition(token, image, url, threshold=4.8):
    endpoint = utils.get_endpoint(ais.AisService.IMAGE_SERVICE)
    _url = 'https://%s%s' % (endpoint, ais.ImageURI.CELEBRITY_RECOGNITION)

    if image:
        image = image.decode("utf-8")

    _data = {
        "image": image,
        "url": url,
        "threshold": threshold
    }

    status_code, resp = utils.request_token(_url, _data, token)
    return resp.decode('utf-8')


#
# access image tagging ，post data by ak,sk
#
def celebrity_recognition_aksk(_ak, _sk, image, url, threshold=4.8):
    endpoint = utils.get_endpoint(ais.AisService.IMAGE_SERVICE)
    _url = 'https://%s%s' % (endpoint, ais.ImageURI.CELEBRITY_RECOGNITION)

    sig = signer.Signer()
    sig.AppKey = _ak
    sig.AppSecret = _sk

    if image:
        image = image.decode("utf-8")

    _data = {
        "image": image,
        "url": url,
        "threshold": threshold,
    }

    kreq = signer.HttpRequest()
    kreq.scheme = "https"
    kreq.host = endpoint
    kreq.uri = "/v1.0/image/celebrity-recognition"
    kreq.method = "POST"
    kreq.headers = {"Content-Type": "application/json"}
    kreq.body = json.dumps(_data)

    status_code, resp = utils.request_aksk(sig, kreq, _url)
    return resp.decode('utf-8')
