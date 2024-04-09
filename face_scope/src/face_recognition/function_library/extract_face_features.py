import cv2
import face_recognition

def extract_face_features_image_path(image_path):
    """
    加载图像文件并提取面部特征编码。

    :param image_path: 图像文件的路径。
    :return: 包含面部特征编码的列表。
    """
    # 加载图像
    image = face_recognition.load_image_file(image_path)

    # 寻找图像中所有人脸的面部特征编码
    # 这里假设输入的图片已经是人脸，因此不需要face_locations
    face_encodings = face_recognition.face_encodings(image)

    # 返回面部特征编码
    return face_encodings

def extract_face_features_for_numpy(face_roi):
    """
    从人脸区域图像中提取面部特征编码。

    :param face_roi: 人脸区域图像，是一个numpy数组。
    :return: 包含面部特征编码的列表。
    """
    # 寻找人脸区域中的面部特征编码
    # 这里假设 face_roi 已经是图像中的人脸区域，因此直接对其进行编码
    face_encodings = face_recognition.face_encodings(face_roi)

    # 返回面部特征编码
    return face_encodings


if __name__ == "__main__":

    # file_path = "./image_static/face_0.png"

    file_path ="./img.png"

    frame = cv2.imread(file_path)
    faces_data, frame_with_faces = detect_faces_in_frame(frame, scaleFactor=1.1, minNeighbors=4,
                                                         show_result=False)

    # 保存图片
    image_filename = "./temp_img.jpg"
    cv2.imwrite(image_filename, frame_with_faces)
    print(f"Saved image: {image_filename}")

    print("face_data : ", len(faces_data[0]), faces_data[0]["image"])

    # 提取特征
    # face_features = extract_face_features_image_path(file_path)
    face_features_numpy = extract_face_features_for_numpy(faces_data[0]["image"])
    print(face_features_numpy)

    # face_scope\src\face_recognition\static\face_images\person_1\1.jpg

    # 在这一步，你可以将 features 序列化并存入数据库
    # print(features)
