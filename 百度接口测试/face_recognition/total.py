import requests
import base64
import os
import cv2
from settings import IMAGE_DIR, get_access_token, FACE_DETECTION_KEYS, SAVING_DIR


class GetRecognition:
    def __init__(self, keyword):
        self.base_url = "https://aip.baidubce.com/rest/2.0/face/"
        self.key_word_url_dict = {
            "人脸检测": os.path.join(self.base_url, "v3", "detect")
        }
        self.headers = {'content-type': 'application/json'}
        self.access_token = get_access_token(FACE_DETECTION_KEYS)
        self.IMAGE_DIR = IMAGE_DIR
        self.saving = SAVING_DIR
        self.keyword = keyword

    def get_json(self):

        final_dict = {}
        final_list = []

        if self.keyword not in self.key_word_url_dict:
            raise KeyError("不存在这样的接口！")

        image_list = os.listdir(self.IMAGE_DIR)

        for i in image_list:
            with open(os.path.join(self.IMAGE_DIR, i), "rb") as f:
                img = base64.b64encode(f.read())

            params = {
                "image": img,
                "image_type": "BASE64",
                "face_field": "faceshape,facetype"
            }

            request_url = f"{self.key_word_url_dict[self.keyword]}?access_token={self.access_token}"
            response = requests.post(request_url, data=params, headers=self.headers)
            if response:
                final_dict.update({"name": i, "response_message": response.json()})
                # print(response.json())
            final_list.append(final_dict)
            final_dict = {}
        return final_list

    def visualization(self, final_list):
        for i in final_list:
            file_path = os.path.join(self.IMAGE_DIR, i["name"])
            response_message = i["response_message"]

            if response_message["error_msg"] != "SUCCESS":
                print("此如片无人脸")
                continue
            for j in response_message["result"]["face_list"]:
                count = 1
                left, top, width, height, total = j["location"].values()
                left = int(left)
                top = int(top)
                width = int(width)
                height = int(height)
                src_img = cv2.imread(file_path)
                img = src_img.copy()
                cv2.line(img, (left, top), (left, top + height), (0, 0, 255))
                cv2.line(img, (left, top), (left + width, top), (0, 0, 255))
                cv2.line(img, (left + width, top), (left + width, top + height), (0, 0, 255))
                cv2.line(img, (left, top + height), (left + width, top + height), (0, 0, 255))

                cv2.imwrite(os.path.join(self.saving, i['name'].split('.')[0]) + ".jpg", img)
                count += 1


obj = GetRecognition("人脸检测")
print(obj.visualization(obj.get_json()))

