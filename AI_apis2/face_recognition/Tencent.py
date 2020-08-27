from tencentcloud.iai.v20200303 import models as iai_models
from tencentcloud.fmu.v20191213 import models as fmu_models
from face_recognition.commons import TencentCommon, TencentMultiCommon
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class TencentSingle(TencentCommon):
    def __init__(self):

        iai_response = self.create_response_engine("iai")
        fmu_response = self.create_response_engine("fmu")

        self.method_dict = {
            "AnalyzeFace": [iai_models.AnalyzeFaceRequest, iai_response.AnalyzeFace],  # 五官定位
            "DetectFace": [iai_models.DeleteFaceRequest, iai_response.DeleteFace],  # 人脸检测与分析
            "DetectLiveFace": [iai_models.DetectLiveFaceRequest, iai_response.DetectLiveFace], # 人脸静态活体检测
            "VerifyFace": [iai_models.VerifyFaceRequest, iai_response.VerifyFace],  # 人脸验证
            "VerifyPerson": [iai_models.VerifyPersonRequest, iai_response.VerifyPerson],  # 人员验证
            "SearchFaces": [iai_models.SearchFacesRequest, iai_response.SearchFaces],  # 人脸搜索
            "SearchFacesReturnsByGroup": [iai_models.SearchFacesReturnsByGroupRequest,
                                          iai_response.SearchFacesReturnsByGroup],  # 人脸搜索分库返回
            "SearchPersons": [iai_models.SearchPersonsRequest, iai_response.SearchPersons],  # 人员搜索
            "SearchPersonsReturnsByGroup": [iai_models.SearchPersonsReturnsByGroupRequest,
                                            iai_response.SearchPersonsReturnsByGroup],  # 人员搜索按库返回
            "Beauty": [fmu_models.BeautifyPicRequest, fmu_response.BeautifyPic]   # 人脸美颜
        }


class TencentMulti(TencentMultiCommon):
    def __init__(self):
        iai_response = self.create_response_engine("iai")
        self.method_dict = {
            "CompareFace": [iai_models.CompareFaceRequest, iai_response.CompareFace],  # 人脸比对
        }

