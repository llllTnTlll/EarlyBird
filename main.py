from cv_helper import *
from structure import *


def seats_occupying():
    # 脚本参数设定
    IS_ON_TIME = True            # 是否在指定时间运行脚本
    START_TIME = "055900"          # 脚本预执行时间
    RUN_TIME = "060000"            # 脚本实际运行时间
    ROUNDS = 10                  # 脚本最大抢选重复执行轮数
    STEP_RETRY = 5               # 关键步骤重试次数

    if IS_ON_TIME:
        on_time(datetime=START_TIME)

    unlock_screen()

    print("------step1------")
    retry(STEP_RETRY)(confirm("confirm0.jpg")(click_into))("step1.jpg")

    print("------step2------")
    retry(STEP_RETRY)(confirm("confirm1.jpg")(click_into))("step2.jpg")

    print("------step3------")
    retry(STEP_RETRY)(confirm("confirm2.jpg")(click_into))("step3.jpg")

    print("------step4------")
    flag1 = retry(STEP_RETRY)(confirm("confirm3.jpg")(click_into))("step4.jpg")
    flag2 = retry(STEP_RETRY)(confirm("confirm4.jpg")(click_into))("refresh.jpg")
    # 确认是否准备完毕
    if flag1 is True and flag2 is True:
        print("READY FOR OCCUPYING...")
    else:
        return

    # 阻塞程序
    # 防止屏幕睡眠
    if IS_ON_TIME:
        keep_on(datetime=RUN_TIME)

    for i in range(ROUNDS):
        click_into("refresh.jpg")
        print("\033[1m================round {}/{}================\033[0m".format(i+1, ROUNDS))

        print("------first order------")
        key1 = retry(1)(confirm("confirm4.jpg")(click_into))("step5.jpg")

        print("------second order------")
        key2 = retry(1)(confirm("confirm4.jpg")(click_into))("step6.jpg")

        if key1 is True or key2 is True:
            break


def main():
    seats_occupying()


if __name__ == '__main__':
    main()
