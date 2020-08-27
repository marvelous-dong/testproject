from settings import BAIDU_OCR_KEYS
from OCR.commons import BaiduCommon
from aip import AipOcr


class Baidu(BaiduCommon):
    def __init__(self):
        engine = AipOcr(**BAIDU_OCR_KEYS)

        self.method_dict = {
            "BasicGeneral": engine.basicGeneral,            # 本地图片基础通用文字识别
            "BasicGeneralUrl": engine.basicGeneralUrl,      # url图片基础通用文字识别
            "BasicAccurate": engine.basicAccurate,          # 通用文字识别（高精度版）
            "General": engine.general,                      # 本地图片通用文字识别（含位置信息版）
            "GeneralUrl": engine.generalUrl,                # url图片通用文字识别（含位置信息版）
            "Accurate": engine.accurate,                    # 通用文字识别（含位置高精度版）
            "EnhancedGeneral": engine.enhancedGeneral,       # 本地图片通用文字识别（含生僻字版）
            "EnhancedGeneralUrl": engine.enhancedGeneralUrl, # url图片通用文字识别（含生僻字版）
            "WebImage": engine.webImage,                     # 本地图片网图文字识别
            "WebImageUrl": engine.webImageUrl,               # url图片网图文字识别
            "IdCard": engine.idcard,                         # 身份证识别
            "Bankcard": engine.bankcard,                     # 银行卡识别
            "DrivingLicense": engine.drivingLicense,          # 驾驶证识别
            "VehicleLicense": engine.vehicleLicense,          # 行驶证识别
            "LicensePlate": engine.licensePlate,              # 车牌识别
            "BusinessLicense": engine.businessLicense,         # 营业执照识别
            "BusinessCard": engine.businessCard,              # 名片识别
            "Passport": engine.passport,                      # 护照识别
            "HK_Macau_exitentrypermit": engine.HKMacauExitentrypermit,   # 港澳通行证识别
            "TaiwanExitentrypermit": engine.taiwanExitentrypermit,      # 台湾通行证识别
            "HouseholdRegister": engine.householdRegister,     # 户口本识别
            "BirthCertificate": engine.birthCertificate,      # 出生证识别
            "Receipt": engine.receipt,                        # 通用票据识别
            "Custom": engine.custom,                          # 自定义模版文字识别
            "Form": engine.form,                              # form表单识别
            "TableRecognitionAsync": engine.tableRecognitionAsync,  # 表格文字识别异步接口
            "TableRecognition": engine.tableRecognition,            # 表格文字识别同步接口
            "VatInvoice": engine.vatInvoice,                  # 增值发票识别
            "QuotaInvoice": engine.quotaInvoice,              # 定额发票识别
            "Invoice": engine.invoice,                         # 通用机打发票识别
            "TrainTicket": engine.trainTicket,                # 火车票识别
            "TaxiReceipt": engine.taxiReceipt,               # 出租车票识别
            "AirTicket": engine.airTicket,                   # 飞机行程单识别
            "InsuranceDocuments": engine.insuranceDocuments,   # 保单识别
            "Lottery": engine.lottery,                        # 彩票识别
            "VINCode": engine.vinCode,                        # VIN码识别
            "VehicleInvoice": engine.vehicleInvoice,          # 机动车销售发票识别
            "VehicleCertificate": engine.vehicleCertificate,  # 车辆合格证识别
            "HandWriting": engine.handwriting,                # 手写文字识别
            "Numbers": engine.numbers,                         # 数字识别
            "Qrcode": engine.qrcode,                          # 二维码识别
        }
