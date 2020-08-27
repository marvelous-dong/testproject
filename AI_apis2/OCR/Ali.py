from OCR.commons import AliCommon


class Ali(AliCommon):
    def __init__(self):
        self.method_dict = {
            "Character": "http://tysbgpu.market.alicloudapi.com/api/predict/ocr_general",   # 通用识别
            "IdCard": "http://dm-51.data.aliyun.com/rest/160601/ocr/ocr_idcard.json",   # 身份证识别
            "DrivingLicense": "http://dm-52.data.aliyun.com/rest/160601/ocr/ocr_driver_license.json",  # 驾驶证识别
            "BandCard": "http://yhk.market.alicloudapi.com/rest/160601/ocr/ocr_bank_card.json",    # 银行卡识别
            "BusinessCard": "http://dm-57.data.aliyun.com/rest/160601/ocr/ocr_business_card.json",    # 名片识别
            "QrCode": "http://qrbarcode.market.alicloudapi.com/api/predict/ocr_qrcode",  # 二维码与条形码识别
            "PassPort": "http://ocrhz.market.alicloudapi.com/rest/160601/ocr/ocr_passport.json",  # 护照识别
            "OfficialSeal": "http://stamp.market.alicloudapi.com/api/predict/ocr_official_seal",  # 公章识别
            "BusinessLicense": "http://dm-58.data.aliyun.com/rest/160601/ocr/ocr_business_license.json",  # 营业执照识别
            "Vin": "http://vin.market.alicloudapi.com/api/predict/ocr_vin",   # Vin码识别
            "TableParse": "https://form.market.alicloudapi.com/api/predict/ocr_table_parse",  # 表格识别
            "Vehicle": "http://dm-53.data.aliyun.com/rest/160601/ocr/ocr_vehicle.json",    # 行驶证识别
            "Advance": "https://ocrapi-advanced.taobao.com/ocrservice/advanced",      # 通用文字识别（高精度）
            "Ecommerce": "https://ocrapi-ecommerce.taobao.com/ocrservice/ecommerce",  # 电商图片文字识别
            "MixedMultiInvoice": "https://ocrapi-mixed-multi-invoice.taobao.com/ocrservice/mixedMultiInvoice",  # 票据混合分区识别
            "Ugc": "https://ocrapi-ugc.taobao.com/ocrservice/ugc",     # 网络ugc文字识别
            "CarInvoice": "https://ocrapi-car-invoice.taobao.com/ocrservice/carInvoice",    # 机动车发票识别
            "VehiclePlate": "http://ocrcp.market.alicloudapi.com/rest/160601/ocr/ocr_vehicle_plate.json",  # 车牌识别
            "GasMeter": "http://gas.market.alicloudapi.com/api/predict/gas_meter_end2end",  # 燃气表水表识别
            "Education": "http://education.market.alicloudapi.com/api/predict/education_ocr",     # 试卷识别
            "HandWriting": "http://handwrite.market.alicloudapi.com/api/predict/ocr_hand_writing",   # 手写数字识别
            "Document": "https://ocrapi-document.taobao.com/ocrservice/document",  # 文档小说图片文字识别
            "DocumentStructure": "https://ocrapi-document-structure.taobao.com/ocrservice/documentStructure",  # 文档结构化还原识别
            "HouseholdRegister": "http://household.market.alicloudapi.com/api/predict/ocr_household_register",  # 户口页识别
            "CardOcr": "http://bbg.market.alicloudapi.com/api/predict/card_ocr",     # 会员卡识别
            "TrainTicket": "http://ocrhcp.market.alicloudapi.com/api/predict/ocr_train_ticket",  # 火车票识别
            "English": "https://ocrapi-english.taobao.com/ocrservice/english",  # 英文专项识别
        }

