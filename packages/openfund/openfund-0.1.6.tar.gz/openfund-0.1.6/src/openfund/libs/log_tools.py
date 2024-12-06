#!/usr/bin/env python
import sys
import os

from loguru import logger
from datetime import datetime

# log_path = "F:\PythonProject\Logs\\"
from openfund.libs.prepare_env import get_path


class Logger:
    def __init__(self, log_name):
        data_path, log_path = get_path()
        self.logger = logger  # 初始化一个logger
        self.logger.remove()  # 清空所有设置
        # 添加控制台输出的格式,sys.stdout为输出到屏幕
        self.logger.add(
            sys.stdout,
            format="<green>{time:YYYYMMDD HH:mm:ss}</green> | "  # 颜色>时间
            "{process.name} | "  # 进程名
            "{thread.name} | "  # 进程名
            "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
            ":<cyan>{line}</cyan> | "  # 行号
            "<level>{level}</level>: "  # 等级
            "<level>{message}</level>",  # 日志内容
        )
        # 输出到文件
        rq = datetime.now().strftime("%Y%m%d")
        if not log_path.endswith("/"):
            log_path = log_path + "/"
        file_name = log_path + log_name + "_" + rq + ".log"  # 文件名称
        self.logger.add(
            file_name,
            level="INFO",
            format="{time:YYYYMMDD HH:mm:ss} - "  # 时间
            "{process.name} | "  # 进程名
            "{thread.name} | "  # 进程名
            "{module}.{function}:{line} - {level} -{message}",  # 模块名.方法名:行号
            rotation="50 MB",
            compression="tar.gz",
        )

    def get_log(self):
        return self.logger
