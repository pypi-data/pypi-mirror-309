import json
import traceback
from datetime import UTC
from typing import Any, Dict, Optional, Tuple

def format_exception(exc_info: Optional[Tuple]) -> Optional[str]:
    """格式化异常信息"""
    if not exc_info:
        return None
    return "".join(traceback.format_exception(*exc_info))

def serialize_record(record: Dict[str, Any]) -> str:
    """序列化日志记录"""
    data = {
        "time": record["time"].astimezone(UTC).isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "request_id": record["extra"].get("request_id", "system"),
        "location": {
            "file": str(record["file"].path),
            "function": record["function"],
            "line": record["line"],
            "module": record["module"],
        },
        "process": {"id": record["process"].id, "name": record["process"].name},
        "thread": {"id": record["thread"].id, "name": record["thread"].name},
    }

    # 添加异常信息
    if record["exception"]:
        data["error"] = {
            "type": record["exception"].type.__name__,
            "message": str(record["exception"].value),
            "traceback": traceback.format_exception(
                record["exception"].type,
                record["exception"].value,
                record["exception"].traceback,
            ),
        }

    # 添加额外的上下文信息
    extra = {k: v for k, v in record["extra"].items() if k != "request_id"}
    if extra:
        data["context"] = extra

    return json.dumps(data, ensure_ascii=False)

def serialize_error_record(record: Dict[str, Any]) -> str:
    """序列化错误日志记录"""
    data = {
        "time": record["time"].astimezone(UTC).isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "request_id": record["extra"].get("request_id", "system"),
        "location": {
            "file": str(record["file"].path),
            "function": record["function"],
            "line": record["line"],
            "module": record["module"],
        },
        "process": {"id": record["process"].id, "name": record["process"].name},
        "thread": {"id": record["thread"].id, "name": record["thread"].name},
    }

    # 增强异常信息记录
    if record["exception"]:
        exc_info = record["exception"]
        data["error"] = {
            "type": exc_info.type.__name__,
            "message": str(exc_info.value),
            "traceback": format_exception(
                exc_info.type, exc_info.value, exc_info.traceback
            ),
            "frames": [
                {
                    "filename": frame.filename,
                    "lineno": frame.lineno,
                    "name": frame.name,
                    "line": frame.line,
                }
                for frame in record["exception"].frames
            ]
            if hasattr(record["exception"], "frames")
            else None,
        }

    # 添加额外的上下文信息
    extra = {k: v for k, v in record["extra"].items() if k != "request_id"}
    if extra:
        data["context"] = extra

    return json.dumps(data, ensure_ascii=False) 