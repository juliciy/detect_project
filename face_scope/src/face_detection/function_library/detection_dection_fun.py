import cv2
import os

from face_scope.src.face_recognition.function_library.extract_face_features import extract_face_features_image_path


def save_face_rois_for_person(faces_data, save_image_path):
    """
    将检测到的人脸区域保存为图像文件，并返回文件路径列表。

    :param faces_data: 检测到的人脸数据列表。
    :param base_dir: 保存图像的基本目录。
    :return: 图像文件路径列表。
    """


    # 初始化一个空列表来存储图像文件路径
    face_images_paths = []

    # 遍历人脸数据
    for i, face_data in enumerate(faces_data):
        # 设置图像文件路径
        img_path = save_image_path

        # 保存人脸区域图像
        cv2.imwrite(img_path, face_data['image'])

        # 添加图像文件路径到列表
        face_images_paths.append(img_path)

    return face_images_paths

def save_face_rois(faces_data, base_dir='./temp'):
    """
    将检测到的人脸区域保存为图像文件，并返回文件路径列表。

    :param faces_data: 检测到的人脸数据列表。
    :param base_dir: 保存图像的基本目录。
    :return: 图像文件路径，位置列表。
    """
    # 确保保存图像的目录存在
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # 初始化一个空列表来存储图像文件路径
    face_images_paths = []
    face_position_in_image = []

    # 遍历人脸数据
    for i, face_data in enumerate(faces_data):
        # 设置图像文件路径
        img_path = os.path.join(base_dir, f'face_{i}.jpg')

        # 保存人脸区域图像
        cv2.imwrite(img_path, face_data['image'])

        face_position_in_image.append(face_data['position'])

        # 添加图像文件路径到列表
        face_images_paths.append(img_path)

    return face_images_paths, face_position_in_image
def detect_faces_in_frame(frame, scaleFactor=1.1, minNeighbors=4, show_result=True):
    """
    在给定的图像帧中检测人脸，并返回检测到的人脸数据和位置以及绘制了人脸框的图像帧。

    :param frame: 输入的图像帧。
    :param scaleFactor: 图像缩放比例，用于检测过程。
    :param minNeighbors: 确定检测到的矩形保留的邻近矩形的数量。
    :param show_result: 是否显示检测结果。
    :return: 一个包含两个元素的元组，第一个元素是一个列表，其中包含检测到的每个人脸的位置和图像数据；第二个元素是绘制了人脸框的图像帧。
    """
    faces_data = []  # 初始化一个空列表来存储人脸数据和位置

    # 创建帧的副本，以便在其上绘制人脸框
    frame_with_faces = frame.copy()

    # 加载 Haar 级联人脸检测分类器
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # 将图像帧转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 检测图像帧中的人脸
    faces = face_cascade.detectMultiScale(gray, scaleFactor, minNeighbors)

    # 处理每个检测到的人脸
    for i, (x, y, w, h) in enumerate(faces):
        face_roi = frame[y:y+h, x:x+w]  # 裁剪出人脸区域

        # 将人脸位置和图像数据添加到列表中
        faces_data.append({'position': (x, y, w, h), 'image': face_roi})

        # 在副本帧上绘制人脸框
        cv2.rectangle(frame_with_faces, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # 如果需要显示结果
    if show_result:
        cv2.imshow('Face Detection', frame_with_faces)
        cv2.waitKey(0)  # 等待按键操作
        cv2.destroyAllWindows()

    # 返回检测到的人脸数据和位置的列表以及绘制了人脸框的图像帧,
    return faces_data, frame_with_faces

def detect_faces_in_frame_for_person(frame, scaleFactor=1.1, minNeighbors=4, show_result=True):
    """
    在给定的图像帧中检测人脸，并返回检测到的人脸数据和位置以及绘制了人脸框的图像帧。

    :param frame: 输入的图像帧。
    :param scaleFactor: 图像缩放比例，用于检测过程。
    :param minNeighbors: 确定检测到的矩形保留的邻近矩形的数量。
    :param show_result: 是否显示检测结果。
    :return: 一个包含两个元素的元组，第一个元素是一个列表，其中包含检测到的每个人脸的位置和图像数据；第二个元素是绘制了人脸框的图像帧。
    """
    faces_data = []  # 初始化一个空列表来存储人脸数据和位置

    # 创建帧的副本，以便在其上绘制人脸框
    frame_with_faces = frame.copy()

    # 加载 Haar 级联人脸检测分类器
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # 将图像帧转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 检测图像帧中的人脸
    faces = face_cascade.detectMultiScale(gray, scaleFactor, minNeighbors)

    # 处理每个检测到的人脸
    for i, (x, y, w, h) in enumerate(faces):
        face_roi = frame[y:y+h, x:x+w]  # 裁剪出人脸区域

        # 将人脸位置和图像数据添加到列表中
        faces_data.append({'position': (x, y, w, h), 'image': face_roi})

        # 在副本帧上绘制人脸框
        cv2.rectangle(frame_with_faces, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # 如果需要显示结果
    if show_result:
        cv2.imshow('Face Detection', frame_with_faces)
        cv2.waitKey(0)  # 等待按键操作
        cv2.destroyAllWindows()

    # 返回检测到的人脸数据和位置的列表以及绘制了人脸框的图像帧
    return faces_data, frame_with_faces


if __name__ == "__main__":

    # 调用函数
    frame = cv2.imread("../static/img_4.png")
    faces_data, frame_with_faces = detect_faces_in_frame(frame, scaleFactor=1.1, minNeighbors=4, show_result=False)
    face_images_paths = save_face_rois(faces_data, "./temp_img/")

    faces_data_features = []
    for i in face_images_paths:
        print(i)
        temp = extract_face_features_image_path(i)
        faces_data_features.append(temp[0])




    # print("detected_img : ", detected_img)
    # for i in faces_data:
    #     print(i["position"], i["image"])
        # break
