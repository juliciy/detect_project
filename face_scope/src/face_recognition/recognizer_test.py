import os
import glob
from PIL import Image
import pickle
import cv2
from face_scope.src.face_recognition.function_library.extract_face_features import extract_face_features


if __name__ == "__main__":

    # 设置文件夹路径

    # 设置基础路径到人脸图像的目录
    base_path = './static/face_images/'

    # 存储所有特征向量的字典
    face_features = {}

    # 遍历所有人的图像
    for person_id in range(1, 41):  # 假定有40个不同的人
        person_folder = f'person_{person_id}'
        person_path = os.path.join(base_path, person_folder)
        face_features[person_folder] = []  # 初始化特征列表

        # 使用glob获取当前人物文件夹中的所有jpg图像文件
        for image_file in glob.glob(os.path.join(person_path, '*.jpg')):
            # 读取图像
            # img = cv2.imread(image_file)
            if image_file is not None:
                # 这里应调用实际的面部特征提取函数
                features = extract_face_features(image_file)
                # 将特征添加到列表中
                face_features[person_folder].append(features)

                # 打印图像路径，用于确认
                print(f'Processed {image_file}')
            else:
                print(f'Failed to load image {image_file}')

    # 将所有特征保存到一个文件中
    with open('./face_features.pkl', 'wb') as f:
        pickle.dump(face_features, f)

    print('所有特征已保存到 face_features.pkl')
