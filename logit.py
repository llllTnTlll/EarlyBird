import sys
import time

import os_helper


def set_log():
    sys.stdout = Logger("./history/log.txt")


class Logger(object):
    def __init__(self, filename, stream=sys.stdout):
        self.terminal = stream
        # 日志文件覆盖模式写入
        self.log = open(filename, 'w')
        # 清理历史运行截图
        os_helper.delete_all("./history/screen_history", False)

    def write(self, message):
        # 终端输出
        self.terminal.write(message)
        if message != "\n" and "----" not in message and "====" not in message:
            if message[1] == "[":
                message = message[5:-4]
            message = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) + message
        self.log.write(message)

    def flush(self):
        pass

