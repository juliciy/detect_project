import cv2

from face_scope.src.face_detection.function_library.detection_dection_fun import detect_faces_in_frame

if __name__ == "__main__":
    path = "./temp_img/img_11.jpg"
    path_faces = "./temp_img/img_11_faces.jpg"
    frame = cv2.imread(path)
    # 进行人脸检测，返回一个包含两个元素的元组，第一个元素是一个列表，其中包含检测到的每个人脸的位置和图像数据；第二个元素是绘制了人脸框的图像帧。
    frame_faces_data, frame_with_faces = detect_faces_in_frame(frame, show_result=False)

    cv2.imwrite(path_faces, frame_with_faces)

    print("frame_faces_data: ", len(frame_faces_data))