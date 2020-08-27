import os

from frsclient import *
from settings import HUAWEI_FACEDETECTION_KEYS
from utils.Exceptions import PlatformAbilityError
from face_recognition.commons import HuaweiCommon, HuaweiMultiCommon


class HuaweiSimple(HuaweiCommon):
    def __init__(self):
        engine = FrsClient(
            auth_info=AuthInfo(
                ak=HUAWEI_FACEDETECTION_KEYS["access_id"],
                sk=HUAWEI_FACEDETECTION_KEYS["access_secret"],
                end_point="https://face.cn-north-4.myhuaweicloud.com"
            ),
            project_id=HUAWEI_FACEDETECTION_KEYS["project_id"]
        )
        self.method_dict = {
            "FaceDetect": [engine.get_detect_service, "detect_face_by_file"],     # 人脸检测
            "LiveDetectService": [engine.get_live_detect_service, "live_detect_by_file"],  # 静默活体检测
        }


class HuaweiMulti(HuaweiMultiCommon):
    def __init__(self):
        engine = FrsClient(
            auth_info=AuthInfo(
                ak=HUAWEI_FACEDETECTION_KEYS["access_id"],
                sk=HUAWEI_FACEDETECTION_KEYS["access_secret"],
                end_point="https://face.cn-north-4.myhuaweicloud.com"
            ),
            project_id=HUAWEI_FACEDETECTION_KEYS["project_id"]
        )
        self.method_dict = {
            "FaceCompare": [engine.get_compare_service, "detect_face_by_file"],     # 人脸比对
        }