from typing import Any

from .base import ReportFormatter


class MypyFormatter(ReportFormatter):
    """Mypy类型检查结果格式化器"""

    def format(self, type_check: dict[str, Any]) -> list[str]:
        lines = ["", "## 类型检查结果"]

        # 获取状态
        status = type_check.get("status", "unknown")
        lines.append(f"状态: {status}")

        # 添加详细输出
        if "output" in type_check and type_check["output"].strip():
            lines.extend(["", "详细:", "```", type_check["output"].strip(), "```"])
        elif "message" in type_check and type_check["message"].strip():
            lines.extend(["", type_check["message"]])
        elif status == "error" and not any(
            [type_check.get("output"), type_check.get("message")]
        ):
            lines.extend(["", "错误：未能获取到详细的类型检查错误信息"])

        return lines
