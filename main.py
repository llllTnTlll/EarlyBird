from cv_helper import *
from structure import *


def seats_occupying():
    # 脚本参数设定
    IS_ON_TIME = False           # 是否在指定时间运行脚本
    RUN_TIME = 202112140530      # 脚本执行时间
    ROUNDS = 5                   # 脚本最大重复执行轮数
    STEP_RETRY = 5               # 关键步骤重试次数

    if IS_ON_TIME:
        on_time(datetime=RUN_TIME)

    unlock_screen()

    for i in range(ROUNDS):
        print("\033[1m================round {}================\033[0m".format(i+1))
        print("------step1------")
        retry(STEP_RETRY)(confirm("confirm0.jpg")(click_into))("step1.jpg")

        print("------step2------")
        retry(STEP_RETRY)(confirm("confirm1.jpg")(click_into))("step2.jpg")

        print("------step3------")
        retry(STEP_RETRY)(confirm("confirm2.jpg")(click_into))("step3.jpg")

        print("------step4------")
        retry(STEP_RETRY)(confirm("confirm3.jpg")(click_into))("step4.jpg")

        print("------step5------")
        key1 = retry(1)(confirm("confirm4.jpg")(click_into))("step5.jpg")

        print("------step6------")
        key2 = retry(1)(confirm("confirm4.jpg")(click_into))("step6.jpg")

        print("------step7------")
        click_into("step7.jpg")

        if key1 is True or key2 is True:
            break


def main():
    seats_occupying()


if __name__ == '__main__':
    main()
