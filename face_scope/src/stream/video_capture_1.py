import glob

import cv2
import datetime
import os

from face_scope.src.connect_to_database.base_data_crud import create_record, insert_batch_insert_into_sys_register
from face_scope.src.face_detection.function_library.detection_dection_fun import detect_faces_in_frame, save_face_rois, \
    save_face_rois_for_person, detect_faces_in_frame_for_person

import cv2
import os
import datetime
import time

from face_scope.src.face_recognition.function_library.calculate_similarity import calculate_similarity
from face_scope.src.face_recognition.function_library.extract_face_features import extract_face_features_for_numpy, \
    extract_face_features_image_path


def match_faces(frame_faces_data_features, person_faces_data_features, person_faces_data_features_file_name):
    """
    匹配图像中的人脸与已知人脸特征列表，并输出匹配或未匹配的文件名。

    :param frame_faces_data_features: 帧图像中所有人脸的特征列表。
    :param person_faces_data_features: 已知的人脸特征列表。
    :param person_faces_data_features_file_name: 已知人脸特征的文件名列表。
    :return: 匹配结果列表，格式为 [匹配的文件名, 'null_i', ...]。
    """
    matches = []
    unmatched_count = 0  # 用于未匹配人脸的编号

    for image_face_encoding in frame_faces_data_features:
        # 初始化最高相似度得分和最佳匹配
        highest_similarity = 0
        best_match_index = None

        for index, known_face_encoding in enumerate(person_faces_data_features):
            similarity, distance = calculate_similarity(known_face_encoding, image_face_encoding)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match_index = index

        # 在这里检查 best_match_index 是否为 None
        if best_match_index is not None:
            # 根据相似度阈值决定是否接受匹配
            if highest_similarity > 0:  # 可根据需要调整阈值
                matches.append(person_faces_data_features_file_name[best_match_index])
            else:
                matches.append(f"null_{unmatched_count}")
                unmatched_count += 1  # 更新未匹配人脸的编号
        else:
            # 没有找到匹配项，处理未匹配的情况
            matches.append(f"null_{unmatched_count}")
            unmatched_count += 1

    return matches


def draw_faces_and_ids(frame, matches, frame_face_position_in_image):
    """
    在图像帧上绘制人脸框和人脸ID。

    :param frame: 原始图像帧。
    :param matches: 人脸ID列表。
    :param frame_face_position_in_image: 人脸在帧图像中的位置列表，每个位置格式为(x, y, w, h)。
    """
    # 确保输入列表长度相等
    if len(matches) != len(frame_face_position_in_image):
        print("matches, frame_face_position_in_image", len(matches), len(frame_face_position_in_image))
        raise ValueError("matches 和 frame_face_position_in_image 列表长度必须相等。")

    for id, position in zip(matches, frame_face_position_in_image):
        print("position : ",position)
        x, y, w, h = position
        # 以图像的左上角为原点（0, 0）绘制,  (x, y)：是矩形左上角的坐标，
        # 在人脸位置绘制矩形框
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # 在框的上方显示人脸ID
        cv2.putText(frame, str(id), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame


def capture_rtsp_stream(rtsp_url, person_faces_data_features, person_faces_data_features_file_name, image_folder="images", ):
    # 在保存文件之前创建文件夹
    os.makedirs(image_folder, exist_ok=True)

    # 从RTSP URL中提取IP地址作为文件名的一部分
    ip_address = rtsp_url.split("//")[1].split(":")[0]

    # 开始捕获RTSP视频流
    cap = cv2.VideoCapture(rtsp_url)

    # 检查视频流是否打开成功
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    last_time = 0  # 初始化上次抓取图片的时间

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            current_time = time.time()

            # 检测到的人脸特征列表
            frame_faces_data_features = []
            frame_faces_data_position = []
            # 每3秒抓取并保存一张图片
            if current_time - last_time > 3:
                # 更新上次抓取图片的时间
                last_time = current_time

                # 使用当前时间戳和IP地址构建文件名
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

                # 进行人脸检测，返回一个包含两个元素的元组，第一个元素是一个列表，其中包含检测到的每个人脸的位置和图像数据；第二个元素是绘制了人脸框的图像帧。
                frame_faces_data, frame_with_faces = detect_faces_in_frame(frame, show_result=False)
                # 帧图像中人脸图像保存的路径，和人脸在帧图像中的位置
                frame_face_images_paths, frame_face_position_in_image = save_face_rois(frame_faces_data, "./temp_img/")

                print("人脸检测的临时文件路径：")
                for i,position in zip(frame_face_images_paths,frame_face_position_in_image):
                    print(i)
                    temp = extract_face_features_image_path(i)
                    # 如查没有提取到人脸的特征，过滤掉
                    if len(temp)>0:
                        print("temp_len : ", len(temp[0]))
                        frame_faces_data_features.append( temp[0] )
                        frame_faces_data_position.append( position )

                if len(frame_faces_data_features) == 0:
                    print(f"{timestamp}_{ip_address}", "没有检测到人脸")
                    # save_image_path = "/www/wwwroot/192.168.0.2/upload/detect_image/"
                    # image_filename = os.path.join(save_image_path, f"{timestamp}_{ip_address}.jpg")
                    # print(f"Saved image: {image_filename}")
                    continue
                else:
                    print(f"{timestamp}_{ip_address}","检测到人脸:",len(frame_faces_data_features))

                print("frame_faces_data_features_len : ", len(frame_faces_data_features), len(frame_faces_data_features[0]))

                # 匹配图像中的人脸与已知人脸特征列表。
                matches = match_faces(frame_faces_data_features, person_faces_data_features, person_faces_data_features_file_name)
                matches_string = "_".join(matches)
                print("matches_data : ", matches_string)

                # 重新绘制帧图像的中人脸框，和人脸ID
                new_frame = draw_faces_and_ids(frame,matches,frame_faces_data_position)

                # 计算未匹配上这一帧的人脸计数,
                matches_null = 0
                for i in matches:
                    if i[:4] == "null":
                        matches_null += 1

                # 保存图片
                # 人 - id_时间_IP_picpath
                # image_filename = os.path.join(image_folder, f"{timestamp}_{ip_address}_{len(matches) - matches_null}_{len(matches)}_{len(frame_faces_data_position)}_{len(frame_faces_data)}.jpg")
                save_image_path = "/www/wwwroot/192.168.0.2/upload/detect_image/"
                image_filename = os.path.join(save_image_path,f"{timestamp}_{ip_address}.jpg")
                image_name_sql = f"{timestamp}_{ip_address}.jpg"
                # "/www/wwwroot/192.168.0.2/upload/detect_image/"

                cv2.imwrite(image_filename, new_frame)
                print(f"Saved image: {image_filename}")

                # 将数据插入数据库
                data_record = []
                print("matches :将数据插入数据库")
                for i,position in zip(matches, frame_faces_data_position):
                    position = str(position)
                    print(i,type(position), position)
                    status_default = 0
                    if i[:4] == "null":
                        status_default = 1
                    # 创建对应数据列表
                    record = create_record(i, ip_address, image_name_sql,position, status_default=status_default)
                    print("添加的数据：", record)
                    data_record.append(record)

                # 插入数据
                insert_batch_insert_into_sys_register(data_record)
                # 清理变量空间
                frame_faces_data_features.clear()
                data_record.clear()

        else:
            break
    # 释放资源
    cap.release()
    cv2.destroyAllWindows()

def extract_filename_without_extension(file_path):
    """
    从给定的文件路径中截取文件名（不包括扩展名）。

    :param file_path: 完整的文件路径。
    :return: 文件名（不含扩展名）。
    """
    # 使用os.path.basename获取路径的最后一部分（即文件名和扩展名）
    base_name = os.path.basename(file_path)
    # 使用os.path.splitext分割文件名和扩展名，并取第一部分（即文件名）
    file_name_without_extension = os.path.splitext(base_name)[0]

    return file_name_without_extension

def find_images_in_path(directory_path):
    images_paths = []
    # 支持的图像文件扩展名列表
    supported_extensions = ['jpg', 'jpeg', 'png', 'gif']

    # 对于每个扩展名，使用glob查找匹配的文件
    for ext in supported_extensions:
        # 注意：这里使用了递归模式 '**'，需要Python 3.5+
        images_paths.extend(glob.glob(os.path.join(directory_path, '**', f'*.{ext}'), recursive=True))

    return images_paths


def insert_subpath_in_image_path(image_path, subpath_insertion):
    """
    在图像路径的目录中插入一个子路径。

    :param image_path: 原始图像文件的路径。
    :param subpath_insertion: 要插入的子路径。
    :return: 修改后的图像路径。
    """
    # 分解原始路径为目录和文件名
    dir_name, file_name = os.path.split(image_path)
    # 获取目录的最后一部分
    last_dir_name = os.path.basename(dir_name)
    # 获取目录的上一级路径
    parent_dir = os.path.dirname(dir_name)

    # 构造新的目录名
    new_dir_name = os.path.join(parent_dir, f"{last_dir_name}_{subpath_insertion}")

    # 重新组合为完整的文件路径
    new_image_path = os.path.join(new_dir_name, file_name)

    return new_image_path

def process_and_extract_faces_from_images(image_dir):
    """
    在给定目录中查找图像文件，检测并保存人脸区域图像，提取人脸特征。

    :param image_dir: 要搜索图像文件的目录。
    :return: 返回两个列表，一个是人脸数据特征的列表，另一个是人脸名字的列表。
    """
    faces_data_features = []    # 人脸数据特征的列表
    faces_data_features_file_name = []   # 人脸名字的列表

    result = find_images_in_path(image_dir)
    for img_path in result:
        print(img_path)
        frame = cv2.imread(img_path)
        faces_data, frame_with_faces = detect_faces_in_frame_for_person(frame, show_result=False)
        subpath_insertion = "temp"
        save_image_path = insert_subpath_in_image_path(img_path, subpath_insertion)
        print("save_image_path : ",save_image_path)

        face_images_paths = save_face_rois_for_person(faces_data, save_image_path)
        for i in face_images_paths:
            print(i)
            file_name = extract_filename_without_extension(i)
            temp = extract_face_features_image_path(i)
            faces_data_features.append(temp[0])
            faces_data_features_file_name.append(file_name)

        print("\n")

    print("faces_data_features : ", len(faces_data_features), len(faces_data_features_file_name))
    print(faces_data_features_file_name)

    # 返回人脸数据特征列表和人脸名字列表
    return faces_data_features, faces_data_features_file_name


if __name__ == "__main__":
    # 使用示例
    # rtsp://:8554/123
    # rtsp_stream_url = 'rtsp://192.168.0.77:554/'

    # rtsp_stream_url = "rtsp://127.0.0.1:8554/"

    # 第一步：提取"./person_image"路径下的人脸数据，先人脸检测，再提取人脸特征，返回人脸特征的列表。
    faces_data_features, faces_data_features_file_name = process_and_extract_faces_from_images("./person_image")

    # 示例用法
    # image_path = "./person_image/person_32.png"
    # subpath_insertion = "temp"
    # new_image_path = insert_subpath_in_image_path(image_path, subpath_insertion)
    #
    # print("Original image path:", image_path)
    # print("New image path:", new_image_path)


    # 每二步：提取每一帧的人脸数据，再提取人脸特征，与第一步的数据做匹配，看相似度。
    rtsp_stream_url = "rtsp://127.0.0.1:8554/"
    # rtsp_stream_url = 'rtsp://192.168.0.77:554/'
    capture_rtsp_stream(rtsp_stream_url, faces_data_features, faces_data_features_file_name)
