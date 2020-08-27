from face_recognition.commons import IflyTekCommon, IflyTekMulti1Common, IflyTekMulti2Common


class IFlyTekSimple(IflyTekCommon):
    def __init__(self):
        self.method_dict = {
            "AgeDetect": "http://tupapi.xfyun.cn/v1/age",  # 年龄识别
            "FaceScore": "http://tupapi.xfyun.cn/v1/face_score",  # 颜值识别
            "SexDetect": "http://tupapi.xfyun.cn/v1/sex",  # 性别识别
            "ExpressionDetect": "http://tupapi.xfyun.cn/v1/expression",  # 表情识别
        }


class IFlyTekMulti1(IflyTekMulti1Common):
    def __init__(self):
        self.method_dict = {
            "FaceCompareSelf": "s67c9c78c",  # 人脸比对（科大讯飞自研算法）
        }


class IFlyTekMulti2(IflyTekMulti2Common):
    def __init__(self):
        self.method_dict = {
            "FaceCompareShangTang": ['http://api.xfyun.cn/v1/service/v1/image_identify/face_verification',
                                     "FaceCompareSense"],  # 人脸比对（商汤算法）
            "WaterMark": ['http://api.xfyun.cn/v1/service/v1/image_identify/watermark_verification', "WaterMark"],
            # 人脸水印照片比对
        }
