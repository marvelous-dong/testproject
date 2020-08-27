from viapi.fileutils import FileUtils
from settings import ALI_IMAGEDETECTION_KEYS


def get_oss_url(img_path):
    file_utils = FileUtils(ALI_IMAGEDETECTION_KEYS["AccessKey_ID"], ALI_IMAGEDETECTION_KEYS["AccessKey_Secret"])

    if img_path[:5] == "https":
        return file_utils.get_oss_url(img_path, "jpeg", False)
    else:
        return file_utils.get_oss_url(img_path, "jpeg", True)
