from .context import request_id

class RequestIDFilter:
    """确保所有日志都有 request_id"""

    def __call__(self, record):
        # 如果 extra 不存在，创建它
        record["extra"] = getattr(record, "extra", {})

        # 优先使用上下文中的 request_id
        try:
            current_request_id = request_id.get()
            record["extra"]["request_id"] = current_request_id
        except LookupError:
            # 如果上下文中没有，则使用默认值
            if "request_id" not in record["extra"]:
                record["extra"]["request_id"] = "system"

        return True 