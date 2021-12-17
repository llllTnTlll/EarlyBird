import os

import cv2 as cv
import numpy as np


def coordinate_trans(tl, br):
    """
    标准坐标系转换
    :param tl:
    :param br:
    :return:
    """
    # 分辨率缩放系数
    pixel_scale = 2
    # 转换为标准中心坐标
    x = int((tl[0] + (br[0] - tl[0]) / 2) / pixel_scale)
    y = int((tl[1] + (br[1] - tl[1]) / 2) / pixel_scale)
    return x, y


def match_temp(screen, temp_name, confirm_mode):
    """
    对指定内容进行模板匹配
    :param screen:
    :param temp_name:
    :param confirm_mode:
    :return: topleft, bottomright
    """
    # 模板匹配结果
    tl = None
    br = None
    flag = False
    # 确定匹配模式
    if confirm_mode:
        directory = "./resources/confirm_template"
    else:
        directory = "./resources/template"
    # 读取模板
    full_temp_name = os.path.join(directory, temp_name)
    temp = cv.imread(full_temp_name)
    # 取得模板高宽
    th, tw = temp.shape[:2]
    # 进行模板匹配返回最可能目标
    result = cv.matchTemplate(screen, temp, method=cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    # 若成功找到匹配结果
    if max_val > 0.95:
        tl = max_loc
        br = (tl[0] + tw, tl[1] + th)
        flag = True
        return flag, tl, br
    else:
        return flag, tl, br


def match_keypoints(kpsA, kpsB, featuresA, featuresB, ratio=0.75, reprojThresh=4.0):
    """
    匹配特征点
    返回
    :param kpsA: 特征点集A
    :param kpsB: 特征点集B
    :param featuresA: 特征集A
    :param featuresB: 特征集B
    :param ratio: 距离比阈值
    :param reprojThresh: 最大允许重投影错误阈值
    :return:匹配点集，仿射变换矩阵，仿射矩阵状态
    """
    # 建立暴力匹配器
    matcher = cv.BFMatcher()
    # 使用KNN检测来自A、B图的SIFT特征匹配对，K=2
    raw_matches = matcher.knnMatch(featuresA, featuresB, 2)

    matches = []
    for m in raw_matches:
        # 当最近距离跟次近距离的比值小于ratio值时，保留此匹配对
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            # 存储两个点在featuresA, featuresB中的索引值
            matches.append((m[0].trainIdx, m[0].queryIdx))

    # 当筛选后的匹配对大于4时，计算视角变换矩阵
    if len(matches) > 4:
        # 获取匹配对的点坐标
        ptsA = np.float32([kpsA[i] for (_, i) in matches])
        ptsB = np.float32([kpsB[i] for (i, _) in matches])
        # 计算视角变换矩阵
        (H, status) = cv.findHomography(ptsA, ptsB, cv.RANSAC, reprojThresh)
        # 返回结果
        return matches, H, status
    # 如果匹配对小于4时，返回None
    return None


def sift_detection(image):
    """
    输入图像返回特征点集和特征向量
    :param image:
    :return:
    """
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    # 检测SIFT特征点，并计算描述子
    descriptor = cv.SIFT_create()
    (kps, features) = descriptor.detectAndCompute(gray, None)
    # 将结果转换成NumPy数组
    kps = np.float32([kp.pt for kp in kps])
    # 返回特征点集，及对应的描述特征
    return kps, features

