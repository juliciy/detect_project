from PIL import Image
import numpy as np
import os

# 图像路径
image_path = './olivettifaces.jpg'

# 读取图像
I = Image.open(image_path)
I = np.array(I, dtype=np.float64) / 255.0  # 将图像读取为double类型并归一化

# 获取图像的大小
M, N = I.shape
m = M // 20  # 每张小图的高
n = N // 20  # 每张小图的宽

# 输出图像保存路径
output_dir = './face_images'

# 创建输出目录
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 分割并保存小图
for i in range(20):
    for j in range(20):
        # 生成小图
        small_pic = I[i * m:(i + 1) * m, j * n:(j + 1) * n]

        # 保存每张小图，目录按人物编号，文件名按小图编号
        person_dir = os.path.join(output_dir, f'person_{i + 1}')
        if not os.path.exists(person_dir):
            os.makedirs(person_dir)
        Image.fromarray((small_pic * 255).astype(np.uint8)).save(
            os.path.join(person_dir, f'{j + 1}.jpg'))

print(f'所有人脸图像已分割并保存到 {output_dir}')