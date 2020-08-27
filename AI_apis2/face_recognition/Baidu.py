from settings import BAIDU_FACEDETECTION_KEYS
from face_recognition.commons import BaiduCommon, BaiduMultiCommon
from aip import AipFace
import os
import base64


class BaiduSimple(BaiduCommon):
    def __init__(self):
        engine = AipFace(**BAIDU_FACEDETECTION_KEYS)
        self.method_dict = {
            "Detect": engine.detect,       # 人脸检测
            "Search": engine.search,       # 人脸搜索
            "PersonVerify": engine.personVerify,   # 身份验证
            "FaceVerify": engine.faceverify,     # 在线活体检测
            "AttributionEdit": engine.attribution_edit,  # 人脸属性编辑
            "Landmark": engine.landmark,      # 人脸特征点（尚未开通）
            "SuperClear": engine.superclear,    # 清晰度增强（尚未开通）
            "Seg": engine.seg,      # 五官分割（尚未开通）
            "SkinColor": engine.skin_color,    # 肤色检测（尚未开通）
            "SkinSmooth": engine.skin_smooth,  # 皮肤光滑度检测（尚未开通）
            "Acnespotmole": engine.acnespotmole,  # 痘雀痣检测（尚未开通）
            "Eyesattr": engine.eyesattr,     # 黑眼圈眼袋检测（尚未开通）
            "Wrinkle": engine.wrinkle,      # 皱纹检测（尚未开通）
        }


class BaiduMulti(BaiduMultiCommon):
    def __init__(self):
        engine = AipFace(**BAIDU_FACEDETECTION_KEYS)
        self.method_dict = {
            "Match": engine.match,         # 人脸对比
            "Faceverify": engine.faceverify,    # 在线活体检测
        }
