from cv_helper import *
from structure import *


def main():
    click_into("step1.jpg")
    confirm("confirm1.jpg")(click_into)("step2.jpg")
    confirm("confirm2.jpg")(click_into)("step3.jpg")
    confirm("confirm3.jpg")(click_into)("step4.jpg")
    confirm("confirm4.jpg")(click_into)("step5.jpg")


if __name__ == '__main__':
    main()
