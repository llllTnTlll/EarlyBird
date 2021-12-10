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
    cv.cvtColor(img, cv.COLOR_BGRA2RGB)

    # 内存释放
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

    return img


def match_temp(screen, temp_name):
    directory = "./resources/template_img"
    result = cv.matchTemplate(screen, img, method=cv.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)


def main():
    screen = screen_shot()
    cv.imshow("im_opencv", cv.resize(screen, (0, 0), fx=0.5, fy=0.5))
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
