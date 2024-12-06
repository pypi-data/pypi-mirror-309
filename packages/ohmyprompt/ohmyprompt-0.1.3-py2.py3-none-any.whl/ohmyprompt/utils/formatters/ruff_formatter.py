from typing import Any

from .base import ReportFormatter


class RuffFormatter(ReportFormatter):
    """Ruff代码检查结果格式化器"""

    def format(self, data: dict[str, Any]) -> list[str]:
        lines: list[str] = [
            "",
            "",
            "## Ruff 代码检查",
            f"状态: {data.get('status', 'unknown')}",
        ]

        if "output" in data and data["output"]:
            errors: list[str] = []
            error_stats: dict[str, int] = {}

            for error in data["output"].split("\n"):
                if error.strip():
                    try:
                        file_path, line_no, code, error_info = error.split(":", 3)
                        errors.append(f"- {file_path}:{line_no} {error_info}")
                        error_stats[code] = error_stats.get(code, 0) + 1
                    except ValueError:
                        errors.append(f"- {error}")

            if errors:
                lines.extend(["", "### 详细错误", "```text", *errors, "```"])

            if error_stats:
                lines.extend(
                    [
                        "",
                        "### 错误统计",
                        "| 错误代码 | 数量 |",
                        "|----------|------|",
                        *[
                            f"| {code} | {count} |"
                            for code, count in sorted(error_stats.items())
                        ],
                    ]
                )

        if "message" in data:
            lines.extend(["", "### 其他信息", data["message"]])

        return lines
