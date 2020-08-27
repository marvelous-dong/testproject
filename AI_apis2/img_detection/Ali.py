from aliyunsdkimagerecog.request.v20190930 import TaggingImageRequest, DetectImageElementsRequest, \
    RecognizeImageStyleRequest, RecognizeSceneRequest, RecognizeImageColorRequest
from aliyunsdkgoodstech.request.v20191230 import ClassifyCommodityRequest, RecognizeFurnitureSpuRequest, RecognizeFurnitureAttributeRequest
from aliyunsdkobjectdet.request.v20191230 import DetectMainBodyRequest, DetectVehicleRequest, DetectObjectRequest, DetectTransparentImageRequest, DetectWhiteBaseImageRequest, RecognizeVehicleDashboardRequest, RecognizeVehiclePartsRequest, ClassifyVehicleInsuranceRequest, RecognizeVehicleDamageRequest
from aliyunsdkimageaudit.request.v20191230 import ScanImageRequest
from img_detection.commons import AliCommon


class Ali(AliCommon):

    def __init__(self):
        self.method_dict = {
            "Tagging": TaggingImageRequest.TaggingImageRequest,  # 通用图像打标
            "Element": DetectImageElementsRequest.DetectImageElementsRequest,  # 图像元素检测
            "Style": RecognizeImageStyleRequest.RecognizeImageStyleRequest,  # 风格识别
            "Scene": RecognizeSceneRequest.RecognizeSceneRequest,  # 场景识别
            "Commodity": ClassifyCommodityRequest.ClassifyCommodityRequest,  # 商品分类
            "MainBody": DetectMainBodyRequest.DetectMainBodyRequest,  # 主体检测
            "Vehicle": DetectVehicleRequest.DetectVehicleRequest,  # 机动车检测
            "Color": RecognizeImageColorRequest.RecognizeImageColorRequest,  # 颜色识别
            "Furniture": RecognizeFurnitureAttributeRequest.RecognizeFurnitureAttributeRequest,  # 家居属性检测
            "FurnitureSPU": RecognizeFurnitureSpuRequest.RecognizeFurnitureSpuRequest,  # 家居SPU检测
            "Pornography": ScanImageRequest.ScanImageRequest,  # 图像安全识别
            "Object": DetectObjectRequest.DetectObjectRequest,  # 物体检测
            "Transparency": DetectTransparentImageRequest.DetectTransparentImageRequest,  # 透明度检测
            "WhiteBase": DetectWhiteBaseImageRequest.DetectWhiteBaseImageRequest,  # 白底图检测
            "VehicleParts": RecognizeVehiclePartsRequest.RecognizeVehiclePartsRequest,  # 车辆部件检测
            "VehicleInsurance": ClassifyVehicleInsuranceRequest.ClassifyVehicleInsuranceRequest,  # 车险识别
            "VehicleDashboard": RecognizeVehicleDashboardRequest.RecognizeVehicleDashboardRequest,  # 车辆仪表盘识别
            "VehicleDamage": RecognizeVehicleDamageRequest.RecognizeVehicleDamageRequest  # 车辆损伤识别
        }



