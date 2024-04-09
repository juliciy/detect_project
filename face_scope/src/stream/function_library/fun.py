
import os

import cv2

from face_scope.src.face_detection.function_library.detection_dection_fun import detect_faces_in_frame
from face_scope.src.face_recognition.function_library.calculate_similarity import calculate_similarity
from face_scope.src.face_recognition.function_library.extract_face_features import extract_face_features_image_path, \
    extract_face_features_for_numpy


def extract_faces_features_from_directory(directory_path):
    # 存储所有图片的人脸特征
    face_features_list = []

    # 遍历目录下的每个文件
    for filename in os.listdir(directory_path):
        if filename.endswith((".png", ".jpg", ".jpeg")):  # 确认文件是图片
            file_path = os.path.join(directory_path, filename)
            file_new_path = os.path.join(directory_path + "/temp/", filename)
            print("file_path : ", file_path)

            # 加载图片, 尝试提取图片中每个人脸的特征
            frame = cv2.imread(file_path)
            faces_data, frame_with_faces = detect_faces_in_frame(frame, scaleFactor=1.1, minNeighbors=4,
                                                                 show_result=False)

            # 保存图片
            image_filename = file_new_path
            cv2.imwrite(image_filename, frame_with_faces)
            print(f"Saved image: {image_filename}")
            print("face_data : ",faces_data[0]["image"])

            # face_encoding = extract_face_features_image_path(file_path)
            face_encoding = extract_face_features_for_numpy( faces_data[0]["image"] )

            face_features_list.append(face_encoding[0])

    return face_features_list

if __name__ == "__main__":
    path = "../person_image/"
    face_features_list = extract_faces_features_from_directory(path)
    for i in face_features_list:
        print("\n")
        print(type(i),len(i))

    # 计算相似度
    similarity_percentage, distance = calculate_similarity(face_features_list[0], face_features_list[1])
    print(f"两张人脸的相似度为：{similarity_percentage}%,欧式距离为{distance}")
    pass