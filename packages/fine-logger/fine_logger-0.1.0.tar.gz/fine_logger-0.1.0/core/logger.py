import json
import sys
import traceback
from datetime import UTC
from pathlib import Path
from typing import Any, Optional, Tuple

from loguru import logger

from .context import ContextLogger
from .filters import RequestIDFilter
from .formatters import serialize_record, serialize_error_record, format_exception
from .adapter import setup_logging

# 定义日志颜色
LOG_COLORS = {
    "TRACE": "<cyan>",  # 青色
    "DEBUG": "<blue>",  # 蓝色
    "INFO": "<green>",  # 绿色
    "SUCCESS": "<green>",  # 绿色
    "WARNING": "<yellow>",  # 黄色
    "ERROR": "<red>",  # 红色
    "CRITICAL": "<RED><bold>",  # 红色加粗
}

def setup_console_logger(
    log_level: str = "DEBUG",
    enqueue: bool = False,
) -> logger:
    """仅配置控制台日志输出"""
    # 移除默认的handler
    logger.remove()

    # 创建 request_id 过滤器
    request_id_filter = RequestIDFilter()

    # 带颜色的控制台日志格式
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level.icon} {level: <8}</level> | "
        "<cyan>{extra[request_id]}</cyan> | "
        "<blue>{file.path}:{line}</blue> | "
        "<magenta>{function}</magenta> | "
        "<level>{message}</level>"
    )

    # 添加控制台处理器
    logger.add(
        sys.stdout,
        format=console_format,
        colorize=True,
        filter=request_id_filter,
        level=log_level,
        enqueue=enqueue,
        backtrace=True,
        diagnose=True,
        catch=True,
    )

    # 添加对标准库logging的支持
    setup_logging(log_level)

    return logger

def setup_logger(
    log_dir: str = "logs",
    log_level: str = "DEBUG",
    rotation: str = "10 MB",
    retention: str = "1 week",
    compression: str = "zip",
    enqueue: bool = False,
) -> logger:
    """配置完整的日志系统，包括文件输出"""
    # 创建日志目录
    try:
        log_path = Path("/data/logs")
        log_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"can not create /data/logs , use logs, e: {e}")
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)

    # 移除默认的handler
    logger.remove()

    # 创建 request_id 过滤器
    request_id_filter = RequestIDFilter()

    # 带颜色的控制台日志格式
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level.icon} {level: <8}</level> | "
        "<cyan>{extra[request_id]}</cyan> | "
        "<blue>{file.path}:{line}</blue> | "
        "<magenta>{function}</magenta> | "
        "<level>{message}</level>"
    )

    # 文件日志格式（不带颜色）
    file_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
        "{level: <8} | "
        "{extra[request_id]} | "
        "{file.path}:{line} | "
        "{function} | "
        "{message}"
    )

    error_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
        "{level: <8} | "
        "{extra[request_id]} | "
        "{file.path}:{line} | "
        "{function} | "
        "{message}\n"
        "Extra Data: {extra}"
    )

    # 添加处理器
    handlers = [
        # 控制台输出
        {
            "sink": sys.stdout,
            "format": console_format,
            "colorize": True,
            "filter": request_id_filter,
            "level": log_level,
            "enqueue": enqueue,
            "backtrace": True,
            "diagnose": True,
            "catch": True,
        },
        # 普通日志文件
        {
            "sink": str(log_path / "app.log"),
            "format": file_format,
            "filter": request_id_filter,
            "level": log_level,
            "rotation": rotation,
            "retention": retention,
            "compression": compression,
            "enqueue": enqueue,
            "backtrace": True,
            "diagnose": True,
            "catch": True,
        },
        # 错误日志文件
        {
            "sink": str(log_path / "error.log"),
            "format": error_format,
            "filter": request_id_filter,
            "level": "ERROR",
            "rotation": rotation,
            "retention": retention,
            "compression": compression,
            "enqueue": enqueue,
            "backtrace": True,
            "diagnose": True,
            "catch": True,
        },
        # JSON格式应用日志
        {
            "sink": str(log_path / "app.json.log"),
            "serialize": serialize_record,
            "filter": request_id_filter,
            "level": log_level,
            "rotation": rotation,
            "retention": retention,
            "compression": compression,
            "enqueue": enqueue,
            "backtrace": True,
            "diagnose": True,
            "catch": True,
        },
        # JSON格式错误日志
        {
            "sink": str(log_path / "error.json.log"),
            "serialize": serialize_error_record,
            "filter": request_id_filter,
            "level": "ERROR",
            "rotation": rotation,
            "retention": retention,
            "compression": compression,
            "enqueue": enqueue,
            "backtrace": True,
            "diagnose": True,
            "catch": True,
        },
    ]

    # 添加所有处理器
    for handler in handlers:
        logger.add(**handler)

    # 添加对标准库logging的支持
    setup_logging(log_level)

    return logger

def log_error(msg: str, exc_info: Optional[Tuple] = None, **kwargs):
    """记录错误日志"""
    if exc_info:
        # 格式化异常信息
        error_detail = format_exception(exc_info)
        # 使用 logger.opt 来记录异常信息，并附加详细的错误信息
        logger.opt(exception=exc_info).error(f"{msg}\n{error_detail}", **kwargs)
    else:
        logger.error(msg, **kwargs)

# 初始化全局logger（仅控制台输出）
logger = setup_console_logger()
