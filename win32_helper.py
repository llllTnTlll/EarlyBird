from ctypes import *
import win32con
import win32gui
import win32ui
import win32api
import numpy
import time
import cv2 as cv


def mouse_move(x, y):
    """
    鼠标移动
    :param x:
    :param y:
    :return:
    """
    windll.user32.SetCursorPos(x, y)


def mouse_click(x, y):
    """
    鼠标单击
    :param x:
    :param y:
    :return:
    """
    mouse_move(x, y)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def screen_shot():
    """
    利用win32api进行全屏截图
    :return: rgb图像
    """
    # 分辨率缩放系数
    pixel_scale = 2
    # 获取桌面
    hdesktop = win32gui.GetDesktopWindow()
    # 获取监视器分辨率
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
