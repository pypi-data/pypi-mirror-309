from contextvars import ContextVar

# 创建请求ID上下文变量
request_id = ContextVar("request_id", default="system")

class ContextLogger:
    """兼容旧的上下文日志器"""

    @staticmethod
    def set_request_id(req_id: str = None):
        """设置请求ID上下文"""
        request_id.set(req_id or "system")

    @staticmethod
    def clear_context():
        """清除上下文"""
        request_id.set("system") 