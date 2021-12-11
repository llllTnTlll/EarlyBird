import os
import cv2 as cv
import time
import win32_helper


def coordinate_trans(tl, br):
    """
    标准坐标系转换
    :param tl:
    :param br:
    :return:
    """
    # 转换为标准中心坐标
    x = int((tl[0] + (br[0] - tl[0]) / 2) / 2)
    y = int((tl[1] + (br[1] - tl[1]) / 2) / 2)
    return x, y


def match_temp(screen, temp_name):
    """
    对指定内容进行模板匹配
    :param screen:
    :param temp_name:
    :return: topleft, bottomright
    """
    # 模板匹配结果
    tl = 0
    br = 0
    flag = False
    # 读取模板
    directory = r".\resources\template"
    full_temp_name = os.path.join(directory, temp_name)
    temp = cv.imread(full_temp_name)
    # 取得模板高宽
    th, tw = temp.shape[:2]
    # 进行模板匹配返回最可能目标
    result = cv.matchTemplate(screen, temp, method=cv.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    if max_val > 0.8:
        tl = max_loc
        br = (tl[0] + tw, tl[1] + th)
        flag = True
        return flag, tl, br
    else:
        return flag, tl, br


def click_into(temp_name):
    flag = False
    while not flag:
        time.sleep(0.5)
        screen = win32_helper.screen_shot()
        flag, tl, br = match_temp(screen, temp_name)
        if tl == 0 or br == 0:
            continue
        # cv.rectangle(screen, tl, br, (0, 0, 255), 2)
        # cv.imshow("", cv.resize(screen, (0, 0), fx=0.3, fy=0.3))
        # cv.waitKey(2000)
        # cv.destroyAllWindows()
        if flag:
            x, y = coordinate_trans(tl, br)
            win32_helper.mouse_click(x, y)
        else:
            print("None Match")
