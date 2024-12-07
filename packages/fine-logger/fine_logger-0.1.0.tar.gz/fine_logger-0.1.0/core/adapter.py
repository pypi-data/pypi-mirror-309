from typing import Optional
import logging
from loguru import logger

class InterceptHandler(logging.Handler):
    """
    将标准库logging的日志重定向到loguru
    """
    def emit(self, record: logging.LogRecord) -> None:
        # 获取对应的loguru级别
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # 找到调用者的信息
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_logging(level: str = "DEBUG"):
    """
    配置标准库logging使用loguru
    """
    # 移除所有已存在的handlers
    logging.root.handlers = []
    
    # 设置日志级别
    logging.root.setLevel(level)
    
    # 添加InterceptHandler
    logging.root.addHandler(InterceptHandler())
    
    # 处理常用的库的日志
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True 