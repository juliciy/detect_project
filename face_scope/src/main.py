# 输入：是IP的视频流和要匹配的人脸
from face_scope.src.stream.video_capture_1 import process_and_extract_faces_from_images, capture_rtsp_stream
import threading

# 输出：人-id_时间_IP_picpath
# 没有匹配上的，要标记为空，如null_0,null_1


def process_rtsp_streams(rtsp_urls, faces_data_features, faces_data_features_file_name):
    """
    对每个 RTSP 流 URL 启动一个线程来捕获视频流并处理。

    :param rtsp_urls: RTSP 流 URL 的列表。
    :param faces_data_features: 已知的人脸特征数据列表。
    :param faces_data_features_file_name: 已知的人脸特征数据对应的文件名列表。
    """
    def thread_target(url):
        """
        线程目标函数，调用 capture_rtsp_stream 来处理单个 RTSP 流。

        :param url: RTSP 流的 URL。
        """
        capture_rtsp_stream(url, faces_data_features, faces_data_features_file_name)

    # 为每个 RTSP 流 URL 启动一个线程
    threads = []
    for url in rtsp_urls:
        thread = threading.Thread(target=thread_target, args=(url,))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    # 使用示例

    # 第一步：提取"./person_image"路径下的人脸数据，先人脸检测，再提取人脸特征，返回人脸特征的列表。
    faces_data_features, faces_data_features_file_name = process_and_extract_faces_from_images("./stream/person_image")

    # 每二步：提取每一帧的人脸数据，再提取人脸特征，与第一步的数据做匹配，看相似度。
    # rtsp_stream_url = "rtsp://127.0.0.1:8554/"

    rtsp_urls = [
        'rtsp://192.168.0.77:554/',
        # 'rtsp://127.0.0.1:8554/',
    ]

    process_rtsp_streams(rtsp_urls, faces_data_features, faces_data_features_file_name)

    # capture_rtsp_stream(rtsp_stream_url, faces_data_features, faces_data_features_file_name)