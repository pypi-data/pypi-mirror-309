from typing import Any

from ...utils.shell_utils import execute_bash
from .base import BaseTool


class MypyTool(BaseTool):
    def get_tool_name(self) -> str:
        return "mypy"

    def check_installation(self) -> bool:
        cmd = f"cd {self.project_root} && rye run mypy --version"
        stdout, stderr, code = execute_bash(cmd)
        return code == 0

    def run(self) -> dict[str, Any]:
        if not self.check_installation():
            return {"status": "skipped", "message": "mypy 未安装"}

        cmd = f"cd {self.project_root} && rye run {self.build_command()}"
        stdout, stderr, code = execute_bash(cmd)

        output = stdout.strip() or stderr.strip()
        return {
            "status": "ok" if code == 0 else "error",
            "output": output,
            "message": "类型检查完成" if code == 0 else "类型检查发现错误",
        }
