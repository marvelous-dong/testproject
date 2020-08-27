from utils.huawei_image_utils.image_tagging import image_tagging
from utils.huawei_image_utils.recapture_detect import recapture_detect
from utils.huawei_image_utils.celebrity_recognition import celebrity_recognition
from img_detection.commons import HuaweiCommon


class Huawei(HuaweiCommon):
    def __init__(self):
        self.method_dict = {
            "Tagging": image_tagging,  # 图像标签
            "Recapture": recapture_detect,  # 翻拍识别
            "Celebrity": celebrity_recognition,  # 名人识别
        }


