from aip import AipImageClassify
from settings import BAIDU_IMAGEDETECTION_KEYS
from img_detection.commons import BaiduCommon


class Baidu(BaiduCommon):
    def __init__(self):
        engine = AipImageClassify(**BAIDU_IMAGEDETECTION_KEYS)
        self.method_dict = {
            "General": engine.advancedGeneral,  # 通用识别
            "Dish": engine.dishDetect,  # 菜品识别
            "Car": engine.carDetect,  # 车辆识别
            "Logo": engine.logoSearch,  # logo识别
            "Animal": engine.animalDetect,  # 动物识别
            "Plant": engine.plantDetect,  # 植物识别
            "Object": engine.objectDetect,  # 目标识别
            "Landmark": engine.landmark,  # 地标识别
            "Flower": engine.flower,  # 花卉识别
            "Ingredient": engine.ingredient,  # 元素识别
            "Redwine": engine.redwine,  # 红酒识别
            "Currency": engine.currency,  # 货币识别
        }

