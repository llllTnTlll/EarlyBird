import time
from functools import wraps

import cv_helper
import win32_helper


def wait_for_seconds(second):
    time.sleep(second)


def on_time(datetime: int):
    """
    定时器
    达到指定时间后释放阻塞
    :param datetime:
    :return:
    """
    is_time = False
    while not is_time:
        time.sleep(1)
        time_now = int(time.strftime("%Y%m%d%H%M", time.localtime()))
        if time_now >= datetime:
            print("it's time!!!")
            is_time = True


def confirm(temp_name):
    """
    带参装饰器
    在未确认到目标时阻塞func
    :param temp_name:
    :return:
    """
    def confirm_decorator(func):
        def func_confirm(*args, **kwargs):
            # 确认目标是否存在
            screen = win32_helper.screen_shot()
            flag, _, _ = cv_helper.match_temp(screen, temp_name, confirm_mode=True)
            if flag:
                print("\033[32m{} Confirmation success\033[0m".format(str(temp_name)))
                # 执行原函数
                result = func(*args, **kwargs)
                return result
            else:
                print("\033[31m{} Confirmation failed\033[0m".format(str(temp_name)))
        return func_confirm
    return confirm_decorator


def retry(times: int):
    """
    带参装饰器
    暂时阻塞程序 允许func反复执行n次
    :param times:
    :return:
    """
    def retry_decorator(func):
        @wraps(func)
        def func_retry(*args, **kwargs):
            # 预设超时错误返回值
            result = False
            for i in range(times):
                result = func(*args, **kwargs)
                if result:
                    break
                else:
                    print("\033[33m{} try again\033[0m".format(str(func.__name__)))
            return result
        return func_retry
    return retry_decorator


def unlock_screen():
    win32_helper.mouse_click(100, 100)
    wait_for_seconds(1)
    win32_helper.mouse_click(100, 100)


