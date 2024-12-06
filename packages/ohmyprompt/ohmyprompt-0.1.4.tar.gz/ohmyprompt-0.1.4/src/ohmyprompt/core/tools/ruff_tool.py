from typing import Any

from ...utils.shell_utils import execute_bash
from .base import BaseTool


class RuffTool(BaseTool):
    def get_tool_name(self) -> str:
        return "ruff"

    def check_installation(self) -> bool:
        cmd = f"cd {self.project_root} && rye run ruff --version"
        stdout, stderr, code = execute_bash(cmd)
        return code == 0

    def run(self) -> dict[str, Any]:
        if not self.check_installation():
            return {"status": "skipped", "message": "ruff 未安装"}

        cmd = f"cd {self.project_root} && rye run {self.build_command()}"
        stdout, stderr, code = execute_bash(cmd)

        output = "\n".join(filter(None, [stdout.strip(), stderr.strip()]))
        return {
            "status": "ok" if code == 0 else "error",
            "output": output,
            "message": "代码检查完成" if code == 0 else "代码检查发现问题",
        }
