from img_detection.commons import IflyTekCommon


class IflyTek(IflyTekCommon):
    def __init__(self):
        self.method_dict = {
            "Scene": "http://tupapi.xfyun.cn/v1/scene",  # 场景识别
            "Currency": "http://tupapi.xfyun.cn/v1/currency"  # 物体识别
        }

