from tencentcloud.iir.v20200417 import models as iir_models
from tencentcloud.tiia.v20190529 import models as tiia_models
from img_detection.commons import TencentCommon

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class Tencent(TencentCommon):
    def __init__(self):

        tiia_response = self.create_response_engine("tiia")
        iir_response = self.create_response_engine("iir")

        self.method_dict = {
            "DetectProduct": [tiia_models.DetectProductRequest, tiia_response.DetectProduct],  # 图像理解 - 商品识别
            "Car": [tiia_models.RecognizeCarRequest, tiia_response.RecognizeCar],  # 车辆识别
            "Celebrity": [tiia_models.DetectCelebrityRequest, tiia_response.DetectCelebrity],  # 公众人物识别
            "Label": [tiia_models.DetectLabelRequest, tiia_response.DetectLabel],  # 商品标签识别
            "Disgust": [tiia_models.DetectDisgustRequest, tiia_response.DetectDisgust],  # 恶心识别
            "Misbehavior": [tiia_models.DetectMisbehaviorRequest, tiia_response.DetectMisbehavior],  # 不良行为识别
            "Quality": [tiia_models.AssessQualityRequest, tiia_response.AssessQuality],  # 图像质量评估
            "Enhance": [tiia_models.EnhanceImageRequest, tiia_response.EnhanceImage],  # 图像增强
            "RecognizeProduct": [iir_models.RecognizeProductRequest,
                                 iir_response.RecognizeProduct],  # 智能识图 - 商品识别
        }
