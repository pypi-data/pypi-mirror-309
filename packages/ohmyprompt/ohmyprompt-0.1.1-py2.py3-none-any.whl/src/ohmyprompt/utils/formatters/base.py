from abc import ABC, abstractmethod
from typing import Any


class ReportFormatter(ABC):
    """报告格式化器基类"""

    @abstractmethod
    def format(self, data: dict[str, Any]) -> list[str]:
        """格式化数据为markdown格式的字符串列表

        Args:
            data: 工具输出的原始数据

        Returns:
            list[str]: 格式化后的Markdown文本行列表，遵循以下格式规范：
            1. 每个部分以两个空行开始
            2. 标题使用 ## 二级标题
            3. 子标题使用 ### 三级标题
            4. 详细信息使用 #### 四级标题
            5. 代码块使用 ``` 包裹，并指定语言
            6. 列表项使用 - 开头
            7. 状态信息使用 "状态: xxx" 格式
        """
        pass
