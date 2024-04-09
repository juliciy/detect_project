import face_recognition

from face_scope.src.face_recognition.function_library.extract_face_features import extract_face_features_image_path


def calculate_similarity(face_encoding1, face_encoding2):
    """
    计算两个面部编码之间的相似度。

    :param face_encoding1: 第一个面部特征编码。
    :param face_encoding2: 第二个面部特征编码。
    :return: 相似度百分比。
    """
    if face_encoding1 is not None and face_encoding2 is not None:
        # 计算两个面部编码之间的欧式距离
        distance = face_recognition.face_distance([face_encoding1], face_encoding2)

        # 假设 distance = 0 时相似度为 100%，distance 增大则相似度降低
        # 阈值根据经验设定，可以调整
        threshold = 0.7
        similarity = max(0, min(100, 100 - (distance / threshold) * 100))
        return similarity, distance
    else:
        return 0  # 如果任一编码为空，相似度返回 0

if __name__ == "__main__":

    # 提取两张人脸图像的特征编码
    encoding_1 = extract_face_features_image_path("../static/face_images/person_20/16.jpg")[0]
    print("encoding_1 : ",encoding_1)
    encoding_2 = extract_face_features_image_path("../static/face_images/person_20/15.jpg")[0]
    print("encoding_2 : ", encoding_2)

    # 计算相似度
    similarity_percentage = calculate_similarity(encoding_1, encoding_2)
    print(f"两张人脸的相似度为：{similarity_percentage}%")
