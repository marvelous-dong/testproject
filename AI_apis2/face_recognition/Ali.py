from aliyunsdkfacebody.request.v20191230 import DetectFaceRequest, RecognizeFaceRequest, CompareFaceRequest, \
    RecognizePublicFaceRequest, RecognizeExpressionRequest, DetectMaskRequest, BodyPostureRequest, HandPostureRequest, \
    RecognizeActionRequest, DetectPedestrianRequest, DetectBodyCountRequest, DetectLivingFaceRequest, VerifyFaceMaskRequest
from face_recognition.commons import AliCommon, AliMultiCommon


class AliSimple(AliCommon):
    def __init__(self):
        self.method_dict = {
            "DetectFace": DetectFaceRequest.DetectFaceRequest,    # 人脸定位检测
            "PublicFace": RecognizePublicFaceRequest.RecognizePublicFaceRequest,    # 公众人物识别
            "Expression": RecognizeExpressionRequest.RecognizeExpressionRequest,   # 表情识别
            "Mask": DetectMaskRequest.DetectMaskRequest,      # 人脸口罩识别
            "RecognizeFace": RecognizeFaceRequest.RecognizeFaceRequest,    # 人脸属性识别
            "BodyPosture": BodyPostureRequest.BodyPostureRequest,    # 人体姿态关键点识别
            "HandPostrue": HandPostureRequest.HandPostureRequest,   # 手势姿态关键点识别
            "RecognizeAction": RecognizeActionRequest.RecognizeActionRequest,   # 动作行为识别
            "Pedestrian": DetectPedestrianRequest.DetectPedestrianRequest,    # 行人检测
            "BodyCount": DetectBodyCountRequest.DetectBodyCountRequest,    # 人体计数
            "LivingFace": DetectLivingFaceRequest.DetectLivingFaceRequest,    # 人脸活体检测
        }


class AliMulti(AliMultiCommon):
    def __init__(self):
        self.method_dict = {
            "CompareFace": CompareFaceRequest.CompareFaceRequest,    # 人脸比对（1：1比对）
            "VerifyFaceMask": VerifyFaceMaskRequest.VerifyFaceMaskRequest,   # 人脸口罩比对
        }


class AliEdit:
    pass
