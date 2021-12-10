import os

import win32con
import win32gui
import win32ui
import win32api
import numpy
import cv2 as cv


def screen_shot():
    """
    利用win32api进行全屏截图
    :return: rgb图像
    """
    # 分辨率缩放系数
    pixel_scale = 2
    # 获取桌面
    hdesktop = win32gui.GetDesktopWindow()
    # 分辨率适应
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN) * pixel_scale
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN) * pixel_scale
    # 创建设备描述表
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    # 创建一个内存设备描述表
    mem_dc = img_dc.CreateCompatibleDC()
    # 创建位图对象
    screenshot = win32ui.CreateBitmap()
    # 开辟存储空间
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    # 截图保存至screenshot
    mem_dc.SelectObject(screenshot)
    # 截图至内存设备描述表
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (0, 0), win32con.SRCCOPY)
    # 将截图保存到文件中
    # screenshot.SaveBitmapFile(mem_dc, 'screenshot.bmp')

    # 格式转换
    signedIntsArray = screenshot.GetBitmapBits(True)
    img = numpy.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)
    img = cv.cvtColor(img, cv.COLOR_BGRA2BGR)

    # 内存释放
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

    return img


def match_temp(screen, temp_name):
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
    result = cv.matchTemplate(screen, temp, method=cv.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    if max_val > 10**8:
        tl = max_loc
        br = (tl[0] + tw, tl[1] + th)
        flag = True
        return flag, tl, br
    else:
        return flag, tl, br


def main():
    screen = screen_shot()
    flag, tl, br = match_temp(screen, "user_rules.jpg")
    if flag:
        cv.rectangle(screen, tl, br, (0, 0, 255), 2)
        cv.imshow("im_opencv", cv.resize(screen, (0, 0), fx=0.5, fy=0.5))
        cv.waitKey(0)
        cv.destroyAllWindows()
    else:
        print("None Match")


if __name__ == '__main__':
    main()
