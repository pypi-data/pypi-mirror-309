from .base import ReportFormatter
from .mypy_formatter import MypyFormatter
from .radon_formatter import RadonFormatter
from .ruff_formatter import RuffFormatter


class FormatterFactory:
    """格式化器工厂"""

    _formatters: dict[str, type[ReportFormatter]] = {
        "ruff_check": RuffFormatter,
        "type_check": MypyFormatter,
        "complexity": RadonFormatter,
    }

    @classmethod
    def get_formatter(cls, tool_name: str) -> ReportFormatter:
        formatter_class = cls._formatters.get(tool_name)
        if formatter_class is None:
            raise ValueError(f"未找到{tool_name}对应的格式化器")
        return formatter_class()
