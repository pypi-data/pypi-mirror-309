from datetime import datetime
from pathlib import Path


class WebReportManager:
    """Web 界面的报告管理功能"""

    def __init__(self, history_path: Path):
        self.history_path = history_path

    def get_reports(self) -> list[dict]:
        """获取所有报告的列表"""
        reports = []
        for file in sorted(self.history_path.glob("*.md"), reverse=True):
            try:
                content = file.read_text(encoding="utf-8")
                reports.append(
                    {
                        "id": file.stem,
                        "timestamp": datetime.fromtimestamp(int(file.stem)),
                        "data": {
                            "content": content,
                            "structure": [],
                            "linter": {"status": "ok"},
                            "tests": {"status": "ok"},
                        },
                    }
                )
            except Exception as e:
                print(f"读取报告失败: {e}")
                continue
        return reports

    def remove_report(self, report_id: str) -> None:
        """删除指定的报告"""
        report_file = self.history_path / f"{report_id}.md"
        if report_file.exists():
            report_file.unlink()
        else:
            raise FileNotFoundError(f"报告 {report_id} 不存在")
