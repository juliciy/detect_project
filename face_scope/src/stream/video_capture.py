import cv2
import datetime
import os

from face_scope.src.face_detection.function_library.detection_dection_fun import detect_faces_in_frame

import cv2
import os
import datetime
import time

from face_scope.src.face_recognition.function_library.extract_face_features import extract_face_features_for_numpy


def capture_rtsp_stream(rtsp_url, image_folder="images"):
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
            print("Processing a new frame...")  # 添加打印语句以便于调试

            current_time = time.time()
            face_features_list = []

            # 每5秒抓取并显示一张图片
            if current_time - last_time > 5:
                # 更新上次抓取图片的时间
                last_time = current_time

                # 调用人脸检测函数（请确保该函数返回人脸数据和绘制了人脸框的帧）
                faces_data, frame_with_faces = detect_faces_in_frame(frame,show_result=False)
                # for i in faces_data:
                #     temp = extract_face_features_for_numpy( i["image"][0] )
                #     face_features_list.append(temp)
                #
                # print("face_len : ", len(face_features_list))


                # 显示视频帧
                # cv2.imshow('RTSP Stream Snapshot', frame_with_faces)
                # print(f"{ip_address}_{int(last_time)}.jpg")

                # 可选：保存图片
                image_filename = os.path.join(image_folder, f"{ip_address}_{int(last_time)}.jpg")
                cv2.imwrite(image_filename, frame_with_faces)

            # 检测按键事件，按 'q' 键退出
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        else:
            break

if __name__ == "__main__":
    # 使用示例
    # rtsp://:8554/123
    rtsp_stream_url = 'rtsp://192.168.0.77:554/'
    # rtsp_stream_url = "rtsp://127.0.0.1:554/"

    # capture_rtsp_stream(rtsp_stream_url)
    capture_rtsp_stream(rtsp_stream_url)
