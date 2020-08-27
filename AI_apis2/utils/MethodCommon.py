import os


class TotalCommon:

    def go(self, keyword, img_path, **param):

        if os.path.isdir(img_path):
            final_list = []
            image_list = os.listdir(img_path)

            for i in image_list:
                img_local_path = os.path.join(img_path, i)
                final_list.append(self.single_file_response(keyword, img_local_path, self.method_dict, **param))

            return final_list

        return self.single_file_response(keyword, img_path, self.method_dict, **param)


class TotalCommonMulti:

    def go(self, keyword, imgA_path, imgB_path, **param):
        if not os.path.isdir(imgB_path):
            raise Exception("图片库必须是文件夹！")

        elif os.path.isdir(imgA_path):
            final_list = []
            imageA_list = os.listdir(imgA_path)
            imageB_list = os.listdir(imgB_path)

            for i in imageA_list:
                for j in imageB_list:
                    imgA_local_path = os.path.join(imgA_path, i)
                    imgB_local_path = os.path.join(imgB_path, j)
                    final_list.append(self.single_file_response(keyword, imgA_local_path, imgB_local_path, self.method_dict, **param))

            return final_list

        final_list = []
        imageB_list = os.listdir(imgB_path)

        for i in imageB_list:
            imgB_local_path = os.path.join(imgB_path, i)
            final_list.append(self.single_file_response(keyword, imgA_path, imgB_local_path, self.method_dict, **param))

        return final_list
