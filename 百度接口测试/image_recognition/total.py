import requests
import base64
import os
from settings import IMAGE_DIR, get_access_token, IMAGE_RECOGNIZATION_KEYS


class GetRecognition:
    def __init__(self, keyword):
        self.base_url = "https://aip.baidubce.com/rest/2.0/image-classify"
        self.key_word_url_dict = {
            "货币": os.path.join(self.base_url, "v1", "currency"),
            "商标": os.path.join(self.base_url, "v2", "logo"),
            "红酒": os.path.join(self.base_url, "v1", "redwine"),
            "烹饪": os.path.join(self.base_url, "v2", "dish")
        }
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}
        self.access_token = get_access_token(IMAGE_RECOGNIZATION_KEYS)
        self.IMAGE_DIR = IMAGE_DIR
        self.keyword = keyword

    def get_json(self):
        if self.keyword not in self.key_word_url_dict:
            raise KeyError("不存在这样的接口！")

        image_list = os.listdir(self.IMAGE_DIR)

        for i in image_list:
            with open(os.path.join(self.IMAGE_DIR, i), "rb") as f:
                img = base64.b64encode(f.read())

            params = {"image": img} if self.keyword == "红酒" else {"custom_lib": True, "image": img}
            request_url = f"{self.key_word_url_dict[self.keyword]}?access_token={self.access_token}"

            response = requests.post(request_url, data=params, headers=self.headers)

            if response:
                print(response.json())


obj = GetRecognition("烹饪")
obj.get_json()
