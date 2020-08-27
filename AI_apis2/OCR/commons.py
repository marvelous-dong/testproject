import hmac
import os
import base64
import json
import requests
import time
import datetime
import hashlib
import urllib.request
from urllib.error import HTTPError

from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import ocr_client
from tencentcloud.common import credential

from settings import ALI_OCR_KEYS, HUAWEI_OCR_KEYS, TENCENT_OCR_KEYS, IFLYTEK_OCR_KEYS, IFLYTEK_OCR_FORMULA_KEYS, \
    IFLYTEK_OCR_CONTENT_KEYS
from utils.Ali_make_url import get_oss_url
from utils.huawei_ocr_utils import HWOcrClientToken
from utils.Exceptions import PlatformAbilityError
from utils.MethodCommon import TotalCommon


class AliCommon(TotalCommon):
    def single_file_response(self, keyword, path, method_dict, **param):

        app_code = ALI_OCR_KEYS["APPCODE"]

        try:
            url = method_dict[keyword]
        except KeyError:
            raise PlatformAbilityError("阿里", keyword)

        img_base64data = self.get_img_base64(path)
        filename = os.path.basename(path)

        if keyword == "IdCard":
            configure = {'side': 'face'}
            stat, header, content = self.predict(url, app_code, img_base64data, configure)
        else:
            stat, header, content = self.predict(url, app_code, img_base64data)

        if stat != 200:
            print('Http status code: ', stat)
            print('Error msg in header: ', header['x-ca-error-message'] if 'x-ca-error-message' in header else '')
            print('Error msg in body: ', content)
            print(f"图像{filename}中没有{keyword}")

        return {"image_name": filename, "response_message": content.decode("utf-8")}

    @staticmethod
    def get_img_base64(img_file):
        with open(img_file, 'rb') as infile:
            s = infile.read()
            return base64.b64encode(s).decode('utf-8')

    @staticmethod
    def predict(url, app_code, img_base64, kv_configure=None):
        param = {}
        param['image'] = img_base64
        if kv_configure is not None:
            param['configure'] = kv_configure

        body = json.dumps(param)
        data = bytes(body, "utf-8")

        headers = {
            'Authorization': 'APPCODE %s' % app_code,
            'Content-Type': 'application/json; charset=UTF-8'
        }
        request = urllib.request.Request(url=url, headers=headers, data=data)

        try:
            response = urllib.request.urlopen(request, timeout=10)
            return response.code, response.headers, response.read()
        except urllib.request.HTTPError as e:
            return e.code, e.headers, e.read()
        except HTTPError:
            return HTTPError.code, HTTPError.headers, HTTPError.read()


class BaiduCommon(TotalCommon):

    def single_file_response(self, keyword, path, method_dict, **param):

        with open(path, "rb") as f:
            img = f.read()

        try:
            method = method_dict[keyword]
        except KeyError:
            raise PlatformAbilityError("百度", keyword)

        if not param:
            response = method(img)
        else:
            response = method(img, options=param)

        filename = os.path.basename(path)

        return {"image_name": filename, "response_message": response}


class HuaweiCommon(TotalCommon):

    def single_file_response(self, keyword, path, method_dict, **param):

        img_path = get_oss_url(path)
        username = HUAWEI_OCR_KEYS["username"]
        password = HUAWEI_OCR_KEYS["password"]
        domain_name = HUAWEI_OCR_KEYS["domain"]
        region = "cn-north-4"

        try:
            req_uri = method_dict[keyword]
        except KeyError:
            raise PlatformAbilityError("华为", keyword)

        try:
            ocrClient = HWOcrClientToken.HWOcrClientToken(domain_name, username, password, region)
            response = ocrClient.request_ocr_service_base64(req_uri, img_path, param)
            filename = os.path.basename(path)
            return {"image_name": filename, "response_message": response.text}
        except ValueError as e:
            print(e)


class TencentCommon(TotalCommon):

    def single_file_response(self, keyword, path, method_dict, **param):

        with open(path, "rb") as f:
            img = base64.b64encode(f.read())

        try:
            req = method_dict[keyword][0]()
            req.from_json_string(json.dumps({"ImageBase64": str(img, "utf-8")}))

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
        cred = credential.Credential(**TENCENT_OCR_KEYS)

        client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)

        return client


class IflyTekCommon(TotalCommon):

    def single_file_response(self, keyword, path, method_dict, **param):

        try:
            URL = method_dict[keyword]
        except KeyError:
            raise PlatformAbilityError("科大讯飞", keyword)

        APPID = IFLYTEK_OCR_KEYS["APPID"]
        API_KEY = IFLYTEK_OCR_KEYS["APIKey"]
        language = "en"
        location = "true"
        current_time = str(int(time.time()))

        param_dict = {"language": language, "location": location}

        if param:
            param_dict.update(param)

        params = json.dumps(param_dict)
        param_base64 = base64.b64encode(params.encode('utf-8'))

        m2 = hashlib.md5()
        str1 = API_KEY + current_time + str(param_base64, 'utf-8')
        m2.update(str1.encode('utf-8'))
        check_sum = m2.hexdigest()

        header = {
            'X-CurTime': current_time,
            'X-Param': param_base64,
            'X-Appid': APPID,
            'X-CheckSum': check_sum,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }

        response = requests.post(URL, headers=header, data=self.get_body(path))
        filename = os.path.basename(path)

        return {"image_name": filename, "response_message": response.text}

    @staticmethod
    def get_body(filepath):
        with open(filepath, 'rb') as f:
            img_file = f.read()
        data = {'image': str(base64.b64encode(img_file), 'utf-8')}
        return data


class IflyTekFomulaCommon(TotalCommon):
    def __init__(self):
        self.Date = self.httpdate(datetime.datetime.utcnow())

    def single_file_response(self, keyword, path, method_dict, **param):
        if keyword == "WebITR":
            BusinessArgs = {
                "ent": "math-arith",
                "aue": "raw",
            }
        elif keyword == "WebITRTeach":
            BusinessArgs = {
                "ent": "teach-photo-print",
                "aue": "raw",
            }
        else:
            BusinessArgs = {
                "ent": "fingerocr",
                "mode": "finger+ocr",
                "method": "dynamic",
                "resize_w": 1088,
                "resize_h": 1632,
            }

        body = self.get_body(BusinessArgs, path)
        headers = self.init_header(body)

        try:
            url = method_dict[keyword]
        except KeyError:
            raise PlatformAbilityError("科大讯飞", keyword)

        response = requests.post(url, data=body, headers=headers, timeout=8)
        filename = os.path.basename(path)

        return {"image_name": filename, "response_message": response.text}

    @staticmethod
    def imgRead(path):
        with open(path, 'rb') as fo:
            return fo.read()

    @staticmethod
    def hashlib_256(res):
        m = hashlib.sha256(bytes(res.encode(encoding='utf-8'))).digest()
        result = "SHA-256=" + base64.b64encode(m).decode(encoding='utf-8')
        return result

    @staticmethod
    def httpdate(dt):
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                 "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
                                                        dt.year, dt.hour, dt.minute, dt.second)

    def generateSignature(self, digest):
        signatureStr = "host: " + "rest-api.xfyun.cn" + "\n"
        signatureStr += "date: " + self.Date + "\n"
        signatureStr += "POST" + " " + "/v2/itr" \
                        + " " + "HTTP/1.1" + "\n"
        signatureStr += "digest: " + digest
        signature = hmac.new(bytes(IFLYTEK_OCR_FORMULA_KEYS["APISercet"].encode(encoding='utf-8')),
                             bytes(signatureStr.encode(encoding='utf-8')),
                             digestmod=hashlib.sha256).digest()
        result = base64.b64encode(signature)
        return result.decode(encoding='utf-8')

    def init_header(self, data):
        digest = self.hashlib_256(data)
        sign = self.generateSignature(digest)
        authHeader = 'api_key="%s", algorithm="%s", ' \
                     'headers="host date request-line digest", ' \
                     'signature="%s"' \
                     % (IFLYTEK_OCR_FORMULA_KEYS["APIKey"], "hmac-sha256", sign)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Method": "POST",
            "Host": "rest-api.xfyun.cn",
            "Date": self.Date,
            "Digest": digest,
            "Authorization": authHeader
        }
        return headers

    def get_body(self, BusinessArgs, AudioPath):

        audioData = self.imgRead(AudioPath)
        content = base64.b64encode(audioData).decode(encoding='utf-8')
        postdata = {
            "common": {"app_id": IFLYTEK_OCR_FORMULA_KEYS["APPID"]},
            "business": BusinessArgs,
            "data": {"image": content}
        }
        body = json.dumps(postdata)
        return body


class IflyTekContentCommon(TotalCommon):

    def single_file_response(self, keyword, path, method_dict, **param):

        x_appid = IFLYTEK_OCR_CONTENT_KEYS["APPID"]
        api_key = IFLYTEK_OCR_CONTENT_KEYS["APIKey"]

        try:
            url = method_dict[keyword]
        except KeyError:
            raise PlatformAbilityError("科大讯飞", keyword)

        x_time = str(int(time.time()))

        m2 = hashlib.md5()
        m2.update(str(api_key + x_time).encode('utf-8'))
        x_checksum = m2.hexdigest()

        x_header = {
            'X-Appid': x_appid,
            'X-CurTime': x_time,
            'X-CheckSum': x_checksum,
        }

        with open(path, 'rb') as f:
            img = f.read()
        data = {'file': str(base64.b64encode(img), 'utf-8')}

        response = requests.post(url, data=data, headers=x_header)
        filename = os.path.basename(path)

        return {"image_name": filename, "response_message": response.text}

