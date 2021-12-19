from cv_helper import *
from win32_helper import *


def click_into(temp_name):
    """
    单击模板匹配结果
    :param temp_name:
    :return:
    """
    screen = screen_shot()
    flag, tl, br = match_temp(screen, temp_name, confirm_mode=False)
    # 若未检测到模板匹配结果
    # break
    if not flag:
        print("\033[31m{} click failed\033[0m".format(str(temp_name)))
        return False
    # 若检测到模板匹配结果
    cv.rectangle(screen, tl, br, (0, 0, 255), 2)
    save_path = "./history/screen_history/"
    cv.imwrite(save_path+temp_name, screen)
    x, y = coordinate_trans(tl, br)
    mouse_click(x, y)
    print("{} clicked".format(str(temp_name)))
    return True


def keep_on(datetime):
    """
    阻塞至datetime
    阻塞结束后返回阻塞前活动窗口
    :param datetime:
    :return:
    """
    hwnd = get_foreground_hwnd()
    # 阻塞
    keep = True
    while keep:
        time_now = int(time.strftime("%m%d%H%M%S", time.localtime()))
        if time_now >= int(datetime):
            break
        mouse_click(0, 0)
        time.sleep(1)
    # 将指定窗口调至顶层
    focus_on(hwnd)


def wait_for_seconds(second):
    time.sleep(second)


def on_time(datetime: str):
    """
    定时器
    达到指定时间后释放阻塞
    :param datetime:
    :return:
    """
    is_time = False
    while not is_time:
        time.sleep(1)
        time_now = int(time.strftime("%m%d%H%M%S", time.localtime()))
        # 每10min发出存活信号
        if time_now % 1000 == 0:
            print("program still alive")
        if int(time_now) >= int(datetime):
            print("it's time!!!")
            is_time = True


def unlock_screen():
    key_board_input(13)
    wait_for_seconds(2)
    key_board_input(13)

