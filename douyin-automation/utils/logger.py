"""
日志工具模块
"""
import os
import logging
from datetime import datetime
from colorlog import ColoredFormatter


class Logger:
    """日志管理器"""

    def __init__(self, name='DouyinBot', log_dir='logs', level='INFO'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))

        # 避免重复添加处理器
        if not self.logger.handlers:
            # 控制台处理器（彩色）
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)

            # 彩色格式
            color_formatter = ColoredFormatter(
                "%(log_color)s[%(asctime)s] [%(levelname)s]%(reset)s %(message)s",
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                }
            )
            console_handler.setFormatter(color_formatter)
            self.logger.addHandler(console_handler)

            # 文件处理器
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
                log_file = os.path.join(
                    log_dir,
                    f"douyin_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
                )
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setLevel(logging.DEBUG)

                file_formatter = logging.Formatter(
                    '[%(asctime)s] [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
