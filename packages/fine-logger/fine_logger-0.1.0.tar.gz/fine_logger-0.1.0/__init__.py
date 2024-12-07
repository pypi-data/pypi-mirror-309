from .core import setup_logger, setup_console_logger, ContextLogger, logger, log_error
from .core.context import request_id
import logging
from typing import Optional

# 提供获取logger的函数
def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    获取logger实例，兼容标准库方式
    """
    return logging.getLogger(name)

__all__ = [
    'setup_logger',
    'setup_console_logger',
    'ContextLogger',
    'logger',
    'log_error',
    'request_id',
    'get_logger'
] 