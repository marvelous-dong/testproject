from OCR.commons import IflyTekCommon, IflyTekFomulaCommon, IflyTekContentCommon


class Iflytek(IflyTekCommon):
    def __init__(self):
        self.method_dict = {
            "HandWriting": "http://webapi.xfyun.cn/v1/service/v1/ocr/handwriting",  # 手写文字识别
            "General": "http://webapi.xfyun.cn/v1/service/v1/ocr/general",  # 印刷文字识别
            "RecognizeDocument": "http://webapi.xfyun.cn/v1/service/v1/ocr/recognize_document",  # 印刷文字识别（多语种）
            "BusinessCard": "http://webapi.xfyun.cn/v1/service/v1/ocr/business_card",  # 名片识别
            "IdCard": "http://webapi.xfyun.cn/v1/service/v1/ocr/idcard",  # 身份证识别
            "Bankcard": "http://webapi.xfyun.cn/v1/service/v1/ocr/bankcard",  # 银行卡识别
            "BusinessLicense": "http://webapi.xfyun.cn/v1/service/v1/ocr/business_license",  # 营业执照识别
            "Invoice": "http://webapi.xfyun.cn/v1/service/v1/ocr/invoice",  # 增值税发票识别
        }


class IflyTekFormula(IflyTekFomulaCommon):

    def __init__(self):
        super().__init__()
        self.method_dict = {
            "WebITR": "https://rest-api.xfyun.cn/v2/itr",  # 拍照速算识别
            "WebFinger": "https://tyocr.xfyun.cn/v2/ocr",     # 指尖文字识别
            "WebITRTeach": "https://rest-api.xfyun.cn/v2/itr",  # 公式识别
        }


class IflyTekContent(IflyTekContentCommon):
    def __init__(self):
        self.method_dict = {
            "SexyFilter": 'http://api.xfyun.cn/v1/service/v1/image_identify/sexy_filter',   # 色情识别
            "CelebrityFilter": 'http://api.xfyun.cn/v1/service/v1/image_identify/celebrity_filter',     # 政治人物识别
            "TerrorFilter": 'http://api.xfyun.cn/v1/service/v1/image_identify/terror_filter',   # 暴恐识别
            "AdFilter": 'http://api.xfyun.cn/v1/service/v1/image_identify/ad_filter',     # 广告过滤
        }
