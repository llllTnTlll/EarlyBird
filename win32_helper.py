import time
from ctypes import *

import cv2 as cv
import numpy
import win32api
import win32con
import win32gui
import win32ui
from win32com import client


def mouse_move(x, y):
    """
    鼠标移动
    :param x:
    :param y:
    :return:
    """
    windll.user32.SetCursorPos(x, y)


def mouse_position():
    """
    获取鼠标位置
    :return:
    """
    p = win32api.GetCursorPos()
    return p


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


def mouse_wheel(distance):
    """
    鼠标滚轮滚动
    :param distance:
    :return:
    """
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, distance)


def key_board_input(key_code):
    win32api.keybd_event(key_code, 0, 0, 0)  # enter
    win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键


def get_foreground_hwnd():
    """
    获取当前窗口句柄
    :return:
    """
    hwnd = win32gui.GetForegroundWindow()
    return hwnd


def get_window_rect(hwnd):
    """
    获取窗体位置和大小
    :param hwnd:
    :return:
    """
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    return x, y, w, h


def focus_on(hwnd):
    """
    将指定窗口调至栈顶
    :param hwnd:
    :return:
    """
    shell = client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)


def adj_window(hwnd, position, size):
    """
    根据窗口句柄调整窗体层叠方式、位置、大小
    :param hwnd:
    :param position:
    :param size:
    :return:
    """
    # HWND_BOTTOM：将窗口置于Z序的底部。如果参数hWnd标识了一个顶层窗口，则窗口失去顶级位置，并且被置在其他窗口的底部。
    # HWND_DOTTOPMOST：将窗口置于所有非顶层窗口之上（即在所有顶层窗口之后）。如果窗口已经是非顶层窗口则该标志不起作用。
    # HWND_TOP: 将窗口置于Z序的顶部。
    # HWND_TOPMOST: 将窗口置于所有非顶层窗口之上。即使窗口未被激活窗口也将保持顶级位置。

    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                          position[0], position[1], size[0], size[1],
                          win32con.SWP_SHOWWINDOW)


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
    width = int(win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN) * pixel_scale)
    height = int(win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN) * pixel_scale)
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
