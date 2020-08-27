# -*- coding:utf-8 -*-

import sys
import json
from utils.huawei_image_utils import ais
from utils.huawei_image_utils import utils
from utils.huawei_image_utils import signer

#
# access image tagging
#
def image_tagging(token, image, url, languzge, limit=-1, threshold=0.0):
    endpoint = utils.get_endpoint(ais.AisService.IMAGE_SERVICE)
    _url = 'https://%s%s' % (endpoint, ais.ImageURI.IMAGE_TAGGING)

    if image:
        image = image.decode("utf-8")

    _data = {
        "image": image,
        "url": url,
        "language": languzge,
        "limit": limit,
        "threshold": threshold
    }

    status_code, resp = utils.request_token(_url, _data, token)
    return resp.decode('unicode_escape')


def image_tagging_aksk(_ak, _sk, image, url, languzge, limit=-1, threshold=0.0):
    endpoint = utils.get_endpoint(ais.AisService.IMAGE_SERVICE)
    _url = 'https://%s%s' % (endpoint, ais.ImageURI.IMAGE_TAGGING)

    sig = signer.Signer()
    sig.AppKey = _ak
    sig.AppSecret = _sk

    if image:
        image = image.decode("utf-8")

    _data = {
        "image": image,
        "url": url,
        "language": languzge,
        "limit": limit,
        "threshold": threshold
    }

    kreq = signer.HttpRequest()
    kreq.scheme = "https"
    kreq.host = endpoint
    kreq.uri = "/v1.0/image/tagging"
    kreq.method = "POST"
    kreq.headers = {"Content-Type": "application/json"}
    kreq.body = json.dumps(_data)

    status_code, resp = utils.request_aksk(sig, kreq, _url)
    return resp.decode('unicode_escape')
