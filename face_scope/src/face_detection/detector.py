import cv2

# 加载Haar级联人脸检测分类器
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 读取图像
img = cv2.imread("./static/img_1.png")

# 将图像转换为灰度图，以提高检测速度和效率
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 检测图像中的人脸
faces = face_cascade.detectMultiScale(gray, 1.1, 4)

# 为每个检测到的人脸绘制矩形框
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

# 显示结果图像
cv2.imshow('img', img)
cv2.waitKey()

# 关闭窗口
cv2.destroyAllWindows()
