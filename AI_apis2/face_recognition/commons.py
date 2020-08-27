import os
import json
import base64
import sys
import requests
import time
import hashlib
import datetime
import hmac
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

from aliyunsdkcore.client import AcsClient
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.iai.v20200303 import iai_client
from tencentcloud.fmu.v20191213 import fmu_client

from settings import ALI_FACEDETECTION_KEYS, TENCENT_FACEDETECTION_KEYS, IFLYTEK_FACEDETECTION_KEYS
from utils.Ali_make_url import get_oss_url
from utils.Exceptions import PlatformAbilityError, AssembleHeaderException
from utils.MethodCommon import TotalCommon, TotalCommonMulti


class AliCommon(TotalCommon):

    def single_file_response(self, keyword, path, method_dict, **param):

        accesskeyid = ALI_FACEDETECTION_KEYS["AccessKey_ID"]
        accesssecret = ALI_FACEDETECTION_KEYS["AccessKey_Secret"]
        client = AcsClient(accesskeyid, accesssecret, 'cn-shanghai')

        try:
            request = method_dict[keyword]()
            request.set_accept_format('json')
        except KeyError:
            raise PlatformAbilityError("阿里", keyword)

        img_oss_path = get_oss_url(path)

        try:
            request.set_Url(img_oss_path)
        except AttributeError:
            try:
                request.set_ImageURL(img_oss_path)
            except AttributeError:
                try:
                    request.set_Tasks([{"ImageURL": img_oss_path}])
                except AttributeError:
                    request.set_URLLists([{"URL": img_oss_path}])

        if keyword == "RecognizeAction":
            request.set_type(1)

        response = client.do_action_with_exception(request)
        filename = os.path.basename(path)

        return {"img_name": filename, "response_message": json.loads(response)}


class AliMultiCommon(TotalCommonMulti):
    def single_file_response(self, keyword, pathA, pathB, method_dict, **param):

        try:
            request = method_dict[keyword]()
            request.set_accept_format('json')
        except KeyError:
            raise PlatformAbilityError("阿里", keyword)

        imgA_oss_path = get_oss_url(pathA)
        imgB_oss_path = get_oss_url(pathB)

        accesskeyid = ALI_FACEDETECTION_KEYS["AccessKey_ID"]
        accesssecret = ALI_FACEDETECTION_KEYS["AccessKey_Secret"]
        client = AcsClient(accesskeyid, accesssecret, 'cn-shanghai')

        try:
            request.set_ImageURLA(imgA_oss_path)
            request.set_ImageURLB(imgB_oss_path)
        except AttributeError:
            try:
                request.set_ImageURL(imgA_oss_path)
                request.set_RefUrl(imgB_oss_path)
            except AttributeError:
                pass

        response = client.do_action_with_exception(request)
        filenameA = os.path.basename(pathA)
        filenameB = os.path.basename(pathB)

        return {"imageA_name": filenameA, "imageB_name": filenameB, "response_message": json.loads(response)}


class BaiduCommon(TotalCommon):

    def single_file_response(self, keyword, path, method_dict, **param):

        with open(path, "rb") as f:
            img = base64.b64encode(f.read())

        if not param:
            params = {
                "image": str(img, "utf-8"),
                "image_type": "BASE64",
            }
        else:
            params = {
                "image": str(img, "utf-8"),
                "image_type": "BASE64",
            }
            params.update(param)

        try:
            response = method_dict[keyword](**params)
        except KeyError:
            raise PlatformAbilityError("百度", keyword)

        filename = os.path.basename(path)

        return {"img_name": filename, "response_message": response}


class BaiduMultiCommon(TotalCommonMulti):

    def single_file_response(self, keyword, pathA, pathB, method_dict, **param):

        with open(pathA, "rb") as f, open(pathB, "rb") as g:
            imgA = base64.b64encode(f.read())
            imgB = base64.b64encode(g.read())

        if not param:
            params = [
                {"image": str(imgA, "utf-8"), "image_type": "BASE64"},
                {"image": str(imgB, "utf-8"), "image_type": "BASE64"}
            ]

        else:
            params = [
                {"image": str(imgA, "utf-8"), "image_type": "BASE64"},
                {"image": str(imgB, "utf-8"), "image_type": "BASE64"}
            ]
            for k in params:
                k.update(param)

        try:
            response = method_dict[keyword](**params)
        except KeyError:
            raise PlatformAbilityError("百度", keyword)

        filenameA = os.path.basename(pathA)
        filenameB = os.path.basename(pathB)

        return {"imageA_name": filenameA, "imageB_name": filenameB, "response_message": response}


class HuaweiCommon(TotalCommon):
    def single_file_response(self, keyword, path, method_dict, **param):

        try:
            ds = method_dict[keyword][0]()
        except KeyError:
            raise PlatformAbilityError("华为", keyword)

        try:
            response_method = getattr(ds, method_dict[keyword][1])
        except KeyError:
            raise PlatformAbilityError("华为", keyword)

        if not param:
            res = response_method(path)
        else:
            res = response_method(path, **param)

        filename = os.path.basename(path)

        return {"image_name": filename, "response_message": res.content_origin}


class HuaweiMultiCommon(TotalCommonMulti):
    def single_file_response(self, keyword, pathA, pathB, method_dict, **param):

        try:
            ds = method_dict[keyword][0]()
        except KeyError:
            raise PlatformAbilityError("华为", keyword)

        response_method = getattr(ds, method_dict[keyword][1])

        if not param:
            res = response_method(pathA, pathB)
        else:
            res = response_method(pathA, pathB, **param)

        filenameA = os.path.basename(pathA)
        filenameB = os.path.basename(pathB)

        return {"imageA_name": filenameA, "imageB_name": filenameB, "response_message": res.content_origin}


class TencentCommon(TotalCommon):
    def single_file_response(self, keyword, path, method_dict, **param):

        with open(path, "rb") as f:
            img = base64.b64encode(f.read())

        try:
            req = method_dict[keyword][0]()

            if not param:
                params = {"Image": str(img, "utf-8")}
            else:
                params = {"Image": str(img, "utf-8")}
                params.update(param)

            req.from_json_string(json.dumps(params))
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
        cred = credential.Credential(**TENCENT_FACEDETECTION_KEYS)

        if word == "iai":
            client = iai_client.IaiClient(cred, "ap-shanghai", clientProfile)
        else:
            client = fmu_client.FmuClient(cred, "ap-shanghai", clientProfile)

        return client


class TencentMultiCommon(TotalCommonMulti):
    def single_file_response(self, keyword, pathA, pathB, method_dict, **param):
        with open(pathA, "rb") as f, open(pathB, "rb") as g:
            imgA = base64.b64encode(f.read())
            imgB = base64.b64encode(g.read())

        try:
            req = method_dict[keyword][0]()

            if not param:
                params = {"ImageA": str(imgA, "utf-8"), "ImageB": str(imgB, "utf-8")}
            else:
                params = {"ImageA": str(imgA, "utf-8"), "ImageB": str(imgB, "utf-8")}
                params.update(param)

            req.from_json_string(json.dumps(params))
            resp = method_dict[keyword][1](req)
            filenameA = os.path.basename(pathA)
            filenameB = os.path.basename(pathB)

            return {"imageA_name": filenameA, "imageB_name": filenameB, "response_message": resp.to_json_string()}

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
        cred = credential.Credential(**TENCENT_FACEDETECTION_KEYS)

        client = None

        if word == "iai":
            client = iai_client.IaiClient(cred, "ap-shanghai", clientProfile)

        return client


class IflyTekCommon(TotalCommon):
    def single_file_response(self, keyword, path, method_dict, **param):

        URL = method_dict[keyword]
        APPID = IFLYTEK_FACEDETECTION_KEYS["FaceFeatrue"]["APPID"]
        API_KEY = IFLYTEK_FACEDETECTION_KEYS["FaceFeatrue"]["APIKey"]

        image_name = os.path.basename(path)
        image_oss_url = get_oss_url(path)

        r = requests.post(URL, headers=self.get_header(APPID, API_KEY, image_name, image_oss_url))

        return {"image_name": image_name, "response_message": r.text}

    @staticmethod
    def get_header(APPID, API_KEY, image_name, image_url=None):
        cur_time = str(int(time.time()))
        param_dict = {"image_name": image_name, "image_url": image_url}
        param = json.dumps(param_dict)
        param_base64 = base64.b64encode(param.encode('utf-8'))
        tmp = str(param_base64, 'utf-8')

        m2 = hashlib.md5()
        m2.update((API_KEY + cur_time + tmp).encode('utf-8'))
        check_sum = m2.hexdigest()

        header = {
            'X-CurTime': cur_time,
            'X-Param': param_base64,
            'X-Appid': APPID,
            'X-CheckSum': check_sum,
        }

        return header


class IflyTekMulti1Common(TotalCommonMulti):
    def single_file_response(self, keyword, pathA, pathB, method_dict, **param):
        try:
            response = self.run(
                appid=IFLYTEK_FACEDETECTION_KEYS["FaceCompare"]["APPID"],
                apisecret=IFLYTEK_FACEDETECTION_KEYS["FaceCompare"]["APISecret"],
                apikey=IFLYTEK_FACEDETECTION_KEYS["FaceCompare"]["APIKey"],
                img1_path=pathA,
                img2_path=pathB,
                server_id=method_dict[keyword]
            )
        except KeyError:
            raise PlatformAbilityError("科大讯飞", keyword)

        filenameA = os.path.basename(pathA)
        filenameB = os.path.basename(pathB)

        return {"imgA_name": filenameA, "imgB_name": filenameB, "response_message": response.text}

    @staticmethod
    def sha256base64(data):
        sha256 = hashlib.sha256()
        sha256.update(data)
        digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
        return digest

    def parse_url(self, requset_url):
        stidx = requset_url.index("://")
        host = requset_url[stidx + 3:]
        schema = requset_url[:stidx + 3]
        edidx = host.index("/")

        if edidx <= 0:
            raise AssembleHeaderException(requset_url)

        path = host[edidx:]
        host = host[:edidx]
        return host, path, schema

    def assemble_ws_auth_url(self, request_url, method="GET", api_key="", api_secret=""):
        host, path, schema = self.parse_url(request_url)
        now = datetime.datetime.now()
        date = format_date_time(time.mktime(now.timetuple()))
        signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
        signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            api_key, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        values = {
            "host": host,
            "date": date,
            "authorization": authorization
        }

        return request_url + "?" + urlencode(values)

    @staticmethod
    def gen_body(appid, img1_path, img2_path, server_id):
        with open(img1_path, 'rb') as f:
            img1_data = f.read()
        with open(img2_path, 'rb') as f:
            img2_data = f.read()
        body = {
            "header": {
                "app_id": appid,
                "status": 3
            },
            "parameter": {
                server_id: {
                    "service_kind": "face_compare",
                    "face_compare_result": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "input1": {
                    "encoding": "jpg",
                    "status": 3,
                    "image": str(base64.b64encode(img1_data), 'utf-8')
                },
                "input2": {
                    "encoding": "jpg",
                    "status": 3,
                    "image": str(base64.b64encode(img2_data), 'utf-8')
                }
            }
        }
        return json.dumps(body)

    def run(self, appid, apikey, apisecret, img1_path, img2_path, server_id):
        url = 'http://api.xf-yun.com/v1/private/{}'.format(server_id)
        request_url = self.assemble_ws_auth_url(url, "POST", apikey, apisecret)
        headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'app_id': appid}
        response = requests.post(request_url, data=self.gen_body(appid, img1_path, img2_path, server_id),
                                 headers=headers)

        return response


class IflyTekMulti2Common(TotalCommonMulti):
    def single_file_response(self, keyword, pathA, pathB, method_dict, **param):

        x_appid = IFLYTEK_FACEDETECTION_KEYS[method_dict[keyword][1]]["APPID"]
        api_key = IFLYTEK_FACEDETECTION_KEYS[method_dict[keyword][1]]["APIKey"]
        try:
            url = method_dict[keyword][0]
        except KeyError:
            raise PlatformAbilityError("科大讯飞", keyword)

        x_time = str(int(time.time()))
        param = json.dumps({'auto_rotate': True})
        x_param = base64.b64encode(param.encode('utf-8'))

        m2 = hashlib.md5()
        m2.update(str(api_key + x_time + str(x_param, 'utf-8')).encode('utf-8'))
        x_checksum = m2.hexdigest()

        x_header = {
            'X-Appid': x_appid,
            'X-CurTime': x_time,
            'X-CheckSum': x_checksum,
            'X-Param': x_param,
        }

        with open(pathA, 'rb') as f, open(pathB, "rb") as g:

            f1_base64 = str(base64.b64encode(f.read()), 'utf-8')
            f2_base64 = str(base64.b64encode(g.read()), 'utf-8')

        data = {
            'first_image': f1_base64,
            'second_image': f2_base64,
        }
        response = requests.post(url, data=data, headers=x_header)

        filenameA = os.path.basename(pathA)
        filenameB = os.path.basename(pathB)

        return {"imageA_name": filenameA, "imageB_name": filenameB, "response_message": response.text}


