from structure import *
import os
import cv2 as cv


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
    if max_val > 0.9:
        tl = max_loc
        br = (tl[0] + tw, tl[1] + th)
        flag = True
        return flag, tl, br
    else:
        return flag, tl, br


def click_into(temp_name):
    """
    单击模板匹配结果
    :param temp_name:
    :return:
    """
    wait_for_seconds(0.2)
    screen = win32_helper.screen_shot()
    flag, tl, br = match_temp(screen, temp_name, confirm_mode=False)
    if tl == 0 or br == 0:
        return False
    cv.rectangle(screen, tl, br, (0, 0, 255), 2)
    save_path = "./history/screen_history/"
    cv.imwrite(save_path+temp_name, screen)
    if flag:
        x, y = coordinate_trans(tl, br)
        win32_helper.mouse_click(x, y)
        print("clicked")
        return True
    else:
        print("fault")
        return False


