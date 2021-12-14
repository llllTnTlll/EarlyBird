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


def mouse_position():
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
