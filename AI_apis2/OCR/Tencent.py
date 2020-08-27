from tencentcloud.ocr.v20181119 import models
from OCR.commons import TencentCommon
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class Tencent(TencentCommon):

    def __init__(self):
        ocr_response = self.create_response_engine("ocr")
        self.method_dict = {
            "Bankcard": [models.BankCardOCRRequest, ocr_response.BankCardOCR],  # 银行卡识别
            "BizLicense": [models.BizLicenseOCRRequest, ocr_response.BizLicenseOCR],  # 营业执照识别
            "EnterpriseLicense": [models.EnterpriseLicenseOCRRequest,
                                  ocr_response.EnterpriseLicenseOCR],  # 企业证照识别
            "BusinessCard": [models.BusinessCardOCRRequest, ocr_response.BusinessCardOCR],  # 名片识别
            "EstateCert": [models.EstateCertOCRRequest, ocr_response.EstateCertOCR],  # 不动产权证识别
            "HmtResidentPermit": [models.HmtResidentPermitOCRRequest,
                                  ocr_response.HmtResidentPermitOCR],  # 港澳台居住证识别
            "IDCard": [models.IDCardOCRRequest, ocr_response.IDCardOCR],  # 身份证识别
            "Institution": [models.InstitutionOCRRequest, ocr_response.InstitutionOCR],
            # 事业单位法人证书识别
            "MainlandPermit": [models.MainlandPermitOCRRequest, ocr_response.MainlandPermitOCR],
            # 港澳台来往内地通行证识别
            "MLIDCard": [models.MLIDCardOCRRequest, ocr_response.MLIDCardOCR],  # 马来西亚身份证识别
            "MLIDPasspord": [models.MLIDPassportOCRRequest, ocr_response.MLIDPassportOCR],
            # 护照识别(港澳台地区及境外护照)
            "OrgCodeCert": [models.OrgCodeCertOCRRequest, ocr_response.OrgCodeCertOCR],
            # 组织机构代码证识别
            "Passport": [models.PassportOCRRequest, ocr_response.PassportOCR],  # 护照识别（大陆地区护照）
            "Permit": [models.PermitOCRRequest, ocr_response.PermitOCR],  # 港澳台通行证识别
            "PropOwnerCert": [models.PropOwnerCertOCRRequest, ocr_response.PropOwnerCertOCR],
            # 房产证识别
            "ResidenceBooklet": [models.ResidenceBookletOCRRequest,
                                 ocr_response.ResidenceBookletOCR],  # 户口本识别
            "QueryBarCode": [models.QueryBarCodeRequest, ocr_response.QueryBarCode],  # 条码信息查询
            "DriverLicense": [models.DriverLicenseOCRRequest, ocr_response.DriverLicenseOCR],
            # 驾驶证识别
            "LicensePlate": [models.LicensePlateOCRRequest, ocr_response.LicensePlateOCR],  # 车牌识别
            "VehicleLicense": [models.VehicleLicenseOCRRequest, ocr_response.VehicleLicenseOCR],
            # 行驶证识别
            "VehicleRegCert": [models.VehicleRegCertOCRRequest, ocr_response.VehicleRegCertOCR],
            # 机动车登记证书识别
            "Vin": [models.VinOCRRequest, ocr_response.VinOCR],  # 车辆 VIN 码识别
            "BusInvoice": [models.BusInvoiceOCRRequest, ocr_response.BusInvoiceOCR],  # 汽车票识别
            "CarInvoice": [models.CarInvoiceOCRRequest, ocr_response.CarInvoiceOCR],  # 购车发票识别
            "DutyPaidProof": [models.DutyPaidProofOCRRequest, ocr_response.DutyPaidProofOCR],
            # 完税证明
            "FinanBill": [models.FinanBillOCRRequest, ocr_response.FinanBillOCR],  # 金融票据整单识别
            "FinanBillSlice": [models.FinanBillSliceOCRRequest, ocr_response.FinanBillSliceOCR],
            # 金融票据切片识别
            "FlightInvoice": [models.FlightInvoiceOCRRequest, ocr_response.FlightInvoiceOCR],
            # 机票行程单识别
            "InvoiceGeneral": [models.InvoiceGeneralOCRRequest, ocr_response.InvoiceGeneralOCR],
            # 通用机打发票识别
            "MixedInvoiceDetect": [models.MixedInvoiceDetectRequest,
                                   ocr_response.MixedInvoiceDetect],  # 混贴票据分类
            "MixedInvoice": [models.MixedInvoiceOCRRequest, ocr_response.MixedInvoiceOCR],
            # 混贴票据识别
            "QuotaInvoice": [models.QuotaInvoiceOCRRequest, ocr_response.QuotaInvoiceOCR],
            # 定额发票识别
            "ShipInvoice": [models.ShipInvoiceOCRRequest, ocr_response.ShipInvoiceOCR],  # 轮船票识别
            "TaxiInvoice": [models.TaxiInvoiceOCRRequest, ocr_response.TaxiInvoiceOCR],  # 出租车发票识别
            "TollInvoice": [models.TollInvoiceOCRRequest, ocr_response.TollInvoiceOCR],  # 过路过桥费发票
            "TrainTicket": [models.TrainTicketOCRRequest, ocr_response.TrainTicketOCR],  # 火车票识别
            "VatInvoice": [models.VatInvoiceOCRRequest, ocr_response.VatInvoiceOCR],  # 增值税发票识别
            "VatRollInvoice": [models.VatInvoiceOCRRequest, ocr_response.VatInvoiceOCR],
            # 增值税发票（卷票）识别
            "Waybill": [models.WaybillOCRRequest, ocr_response.WaybillOCR],  # 运单识别
            "Arithmetic": [models.ArithmeticOCRRequest, ocr_response.ArithmeticOCR],  # 算式识别
            "EduPaper": [models.EduPaperOCRRequest, ocr_response.EduPaperOCR],  # 数学试题识别
            "Formula": [models.FormulaOCRRequest, ocr_response.FormulaOCR],  # 数学公式识别
            "InsuranceBill": [models.InsuranceBillOCRRequest, ocr_response.InsuranceBillOCR],
            # 保险单据识别
            "Seal": [models.SealOCRRequest, ocr_response.SealOCR],  # 印章识别
            "Table": [models.TableOCRRequest, ocr_response.TableOCR],  # 表格识别
            "English": [models.EnglishOCRRequest, ocr_response.EnglishOCR],  # 英文识别
            "GeneralAccurate": [models.GeneralAccurateOCRRequest, ocr_response.GeneralAccurateOCR],
            # 通用印刷体识别（高精度版）
            "GeneralBasic": [models.GeneralBasicOCRRequest, ocr_response.GeneralBasicOCR],
            # 通用印刷体识别
            "GeneralEfficient": [models.GeneralEfficientOCRRequest,
                                 ocr_response.GeneralEfficientOCR],  # 通用印刷体识别（精简版）
            "GeneralFast": [models.GeneralFastOCRRequest, ocr_response.GeneralFastOCR],
            # 通用印刷体识别（高速版）
            "GeneralHandWriting": [models.GeneralHandwritingOCRRequest,
                                   ocr_response.GeneralHandwritingOCR],  # 通用手写体识别
            "Qrcode": [models.QrcodeOCRRequest, ocr_response.QrcodeOCR],  # 二维码和条形码识别
            "TextDetect": [models.TextDetectRequest, ocr_response.TextDetect],  # 快速文本检测
        }



