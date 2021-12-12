from cv_helper import *
from structure import *
import win32_helper


def main():
    # on_time("202112120530")
    win32_helper.mouse_click(100, 100)
    wait_for_seconds(1)
    win32_helper.mouse_click(100, 100)
    confirm("confirm0.jpg")(click_into)("step1.jpg")
    confirm("confirm1.jpg")(click_into)("step2.jpg")
    confirm("confirm2.jpg")(click_into)("step3.jpg")
    confirm("confirm3.jpg")(click_into)("step4.jpg")
    wait_for_seconds(1)
    confirm("confirm4.jpg")(click_into)("step5.jpg")
    wait_for_seconds(1)
    confirm("confirm4.jpg")(click_into)("step6.jpg")


if __name__ == '__main__':
    main()
