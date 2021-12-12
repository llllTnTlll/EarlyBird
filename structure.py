import time
import cv_helper
import win32_helper


def wait_for_seconds(second):
    time.sleep(second)


def on_time(datetime: str):
    is_time = False
    while not is_time:
        time.sleep(1)
        time_now = time.strftime("%Y%m%d%H%M", time.localtime())
        if datetime == time_now:
            print("it's time!!!")
            is_time = True


def confirm(temp_name):
    def confirm_decorator(func):
        def func_block(*args, **kwargs):
            flag = False
            while not flag:
                # 读取模板
                screen = win32_helper.screen_shot()
                flag, _, _ = cv_helper.match_temp(screen, temp_name, confirm_mode=True)
                if flag:
                    print("success")
                    # 执行原函数
                    result = func(*args, **kwargs)
                    return result
                else:
                    print("waiting")
        return func_block
    return confirm_decorator


def retry(times: int):
    def retry_decorator(func):
        def func_block(*args, **kwargs):
            result = False
            for i in range(times):
                result = func(*args, **kwargs)
                if result:
                    break
                else:
                    print("try again")
            return result
        return func_block
    return retry_decorator


