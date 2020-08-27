from aliyunsdkcore.client import AcsClient
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.iir.v20200417 import iir_client
from tencentcloud.tiia.v20190529 import tiia_client

from settings import ALI_IMAGEDETECTION_KEYS, HUAWEI_IMAGEDETECTION_KEYS, TENCENT_IMAGEDETECTION_KEYS, \
    IFLYTEK_IMAGEDETECTION_KEYS
from utils.Ali_make_url import get_oss_url
from utils.huawei_image_utils.gettoken import get_token
from utils.huawei_image_utils.utils import encode_to_base64, init_global_env
import os
import base64
import time
import requests
import hashlib
import json

from utils.Exceptions import PlatformAbilityError
from utils.MethodCommon import TotalCommon


class AliCommon(TotalCommon):

    def single_file_response(self, keyword, path, method_dict, **param):

        client = AcsClient(
            ALI_IMAGEDETECTION_KEYS["AccessKey_ID"],
            ALI_IMAGEDETECTION_KEYS["AccessKey_Secret"],
            "cn-shanghai"
        )

        filename = os.path.basename(path)

        try:
            request = method_dict[keyword]()
        except KeyError:
            raise PlatformAbilityError("阿里", keyword)

        if keyword in ["Element", "Style"]:
            request.set_Url(get_oss_url(path))
        else:
            request.set_ImageURL(get_oss_url(path))

        if keyword in ["Color"]:
            request.set_ColorCount(3)

        response = client.do_action_with_exception(request)

        return {"img_name": filename, "response_message": json.loads(response)}


class BaiduCommon(TotalCommon):

    def single_file_response(self, keyword, path, method_dict, **param):

        try:
            method = method_dict[keyword]
        except KeyError:
            raise PlatformAbilityError("百度", keyword)

        with open(path, "rb") as f:
            img = f.read()

        if not param:
            params = {"image": img}
        else:
            params = {"image": img}
            params.update(param)

        response = method(**params)

        filename = os.path.basename(path)

        return {"img_name": filename, "response_message": response}


class HuaweiCommon(TotalCommon):

    def single_file_response(self, keyword, path, method_dict, **param):

        init_global_env('cn-north-4')
        token = get_token(
            HUAWEI_IMAGEDETECTION_KEYS["username"],
            HUAWEI_IMAGEDETECTION_KEYS["password"],
            HUAWEI_IMAGEDETECTION_KEYS["domain"]
        )
        if keyword == "Tagging":
            params = ["zh", 5, 60]
        elif keyword == "Recapture":
            params = [0.75, ["recapture"]]
        else:
            params = [0.48]

        try:
            result = method_dict[keyword](token, encode_to_base64(path), '', *params)
        except KeyError:
            raise PlatformAbilityError("华为", keyword)

        filename = os.path.basename(path)

        return {"img_name": filename, "response_message": result}


class TencentCommon(TotalCommon):

    def single_file_response(self, keyword, path, method_dict, **param):

        with open(path, "rb") as f:
            img = base64.b64encode(f.read())

        try:
            req = method_dict[keyword][0]()
            target_dict = {"ImageBase64": str(img, "utf-8")}

            if param:
                target_dict.update(param)

            req.from_json_string(json.dumps(target_dict))

            resp = method_dict[keyword][1](req)

            filename = os.path.basename(path)

            return {"image_name": filename, "response_message": resp.to_json_string()}

        except TencentCloudSDKException as err:
            print(err)
        except KeyError:
            raise PlatformAbilityError("腾讯", keyword)

    @staticmethod
    def create_response_engine(word):
        httpProfile = HttpProfile()
        httpProfile.endpoint = word + ".tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        cred = credential.Credential(**TENCENT_IMAGEDETECTION_KEYS)

        if word == "iir":
            client = iir_client.IirClient(cred, "ap-shanghai", clientProfile)
        else:
            client = tiia_client.TiiaClient(cred, "ap-shanghai", clientProfile)

        return client


class IflyTekCommon(TotalCommon):

    def single_file_response(self, keyword, path, method_dict, **param):

        img_oss_path = get_oss_url(path)
        filename = os.path.basename(path)
        try:
            response = requests.post(method_dict[keyword], headers=self.getHeader(filename, img_oss_path))
        except KeyError:
            raise PlatformAbilityError("科大讯飞", keyword)

        return {"img_name": filename, "response_message": response.text}


    @staticmethod
    def getHeader(image_name, image_url=""):
        current_time = str(int(time.time()))
        param_dict = {"image_name": image_name, "image_url": image_url}
        param = json.dumps(param_dict)
        param_base64 = base64.b64encode(param.encode('utf-8'))
        tmp = str(param_base64, 'utf-8')

        m2 = hashlib.md5()
        m2.update((IFLYTEK_IMAGEDETECTION_KEYS["APIKey"] + current_time + tmp).encode('utf-8'))
        check_sum = m2.hexdigest()

        header = {
            'X-CurTime': current_time,
            'X-Param': param_base64,
            'X-Appid': IFLYTEK_IMAGEDETECTION_KEYS["APPID"],
            'X-CheckSum': check_sum,
        }
        return header