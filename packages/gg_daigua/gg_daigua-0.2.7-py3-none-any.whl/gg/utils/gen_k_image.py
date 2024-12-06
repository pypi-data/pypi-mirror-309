import cv2
import numpy as np
from tqdm import tqdm


def detect_black_block_widths(image):
    # 1. 转为灰度图
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 2. 二值化
    _, binary_image = cv2.threshold(gray_image, 50, 255, cv2.THRESH_BINARY_INV)
    # 3. 查找轮廓
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 4. 测量黑色方块宽度并筛选符合条件的宽度
    block_widths = []
    width_set = set()
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        width_set.add(w)
        block_widths.append((x, w))
    # 获取最大宽度
    max_width = max(width_set)
    # 筛选出符合条件的方块
    ret = []
    for x, w in block_widths:
        if w < max_width - 1:  # 过滤掉小于最大宽度的方块
            continue
        ret.append((x, w))
    ret.sort()
    return ret


def crop_image_from_left(image, crop_width, fill_color=(255, 255, 255)):
    height, width, channels = image.shape
    crop_width = min(crop_width, width)
    result_image = np.full((height, width, channels), fill_color, dtype=np.uint8)
    result_image[:, :crop_width] = image[:, :crop_width]
    return result_image


def gen_split_k_image(image_path: str):
    # 1. 读取图像
    image = cv2.imread(image_path)
    ret = detect_black_block_widths(image)
    for i, (r1, r2) in enumerate(tqdm(ret, desc="Processing Blocks", unit="block")):
        # 计算截取范围
        tmp = crop_image_from_left(image, r1 + r2 + 4)

        # 保存结果
        output_filename = f"{i + 1}-{r1}-{r2}.png"
        cv2.imwrite(output_filename, tmp)


if __name__ == '__main__':
    main()
