# -*- coding:utf-8 -*-

import sys
import json
from utils.huawei_image_utils import ais
from utils.huawei_image_utils import utils
from utils.huawei_image_utils import signer

#
# access image recapture detect
#
def recapture_detect(token, image, url, threshold=0.95, scene=None):
    endpoint = utils.get_endpoint(ais.AisService.IMAGE_SERVICE)
    _url = 'https://%s%s' % (endpoint, ais.ImageURI.RECAPTURE_DETECT)

    if sys.version_info.major >= 3:
        if image:
            image = image.decode("utf-8")

    _data = {
        "image": image,
        "url": url,
        "threshold": threshold,
        "scene": scene,
    }

    status_code, resp = utils.request_token(_url, _data, token)
    return resp.decode('utf-8')


#
# access image recapture detect ,post data by aksk
#
def recapture_detect_aksk(_ak, _sk, image, url, threshold=0.95, scene=None):
    endpoint = utils.get_endpoint(ais.AisService.IMAGE_SERVICE)
    _url = 'https://%s%s' % (endpoint, ais.ImageURI.RECAPTURE_DETECT)

    sig = signer.Signer()
    sig.AppKey = _ak
    sig.AppSecret = _sk
    if image:
        image = image.decode("utf-8")

    _data = {
        "image": image,
        "url": url,
        "threshold": threshold,
        "scene": scene,
    }

    kreq = signer.HttpRequest()
    kreq.scheme = "https"
    kreq.host = endpoint
    kreq.uri = "/v1.0/image/recapture-detect"
    kreq.method = "POST"
    kreq.headers = {"Content-Type": "application/json"}
    kreq.body = json.dumps(_data)

    status_code, resp = utils.request_aksk(sig, kreq, _url)
    return resp.decode('utf-8')
