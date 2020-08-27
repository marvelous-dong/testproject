from OCR.commons import HuaweiCommon


class Huawei(HuaweiCommon):
    def __init__(self):
        self.method_dict = {
            "IdCard": "/v1.0/ocr/id-card",       # 身份证识别
            "GeneralTable": "/v1.0/ocr/general-table",    # 通用表格识别
            "GeneralText": "/v1.0/ocr/general-text",        # 通用文字识别
            "WebImage": "/v1.0/ocr/web-image",        # 网络图片识别
            "AutoClassification": "/v1.0/ocr/auto-classification",    # 自动分类识别
            "HandWriting": "/v1.0/ocr/handwriting",     # 手写识别
            "VehicleLicense": "/v1.0/ocr/vehicle-license",        # 行驶证识别
            "DriverLicense": "/v1.0/ocr/driver-license",        # 驾驶证识别
            "Passport": "/v1.0/ocr/passport",                # 护照识别
            "BankCard": "/v1.0/ocr/bankcard",               # 银行卡识别
            "BusinessLicense": "/v1.0/ocr/business-license",    # 营业执照识别
            "Transportation": "/v1.0/ocr/transportation-license",  # 道路运输证识别
            "LicensePlate": "/v1.0/ocr/license-plate",          # 车牌识别
            "BusinessCard": "/v1.0/ocr/business-card",         # 名片识别
            "Vin": "/v1.0/ocr/vin",                      # vin 码识别
            "VatInvoice": "/v1.0/ocr/vat-invoice",        # 增值税发票识别
            "MvsInvoice": "/v1.0/ocr/mvs-invoice",        # 机动车销售发票识别
            "TaxiInvoice": "/v1.0/ocr/taxi-invoice",      # 出租车发票识别
            "TrainTicket": "/v1.0/ocr/train-ticket",      # 火车票识别
            "QuotaInvoice": "/v1.0/ocr/quota-invoice",    # 定额发票识别
            "TollInvoice": "/v1.0/ocr/toll-invoice",      # 车辆通行费发票识别
            "FlightItinerary": "/v1.0/ocr/flight-itinerary",   # 飞机行程单识别
            "EnglishForm": "/v1.0/ocr/ocr_form",            # 英文海关单据识别

        }
