import os
import socket

import click
import uvicorn

from .core.tools.project_tools import ProjectTools


def find_free_port(start_port: int = 8000, max_tries: int = 100) -> int | None:
    """查找可用端口"""
    for port in range(start_port, start_port + max_tries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("", port))
                return port
        except OSError:
            continue
    return None


@click.command()
@click.option("--path", "-p", default=".", help="项目路径，默认为当前目录")
def cli(path: str):
    """OhMyPrompt - Python项目分析工具"""
    # 获取项目的绝对路径
    project_root = os.path.abspath(path)

    # 启动 Web 服务
    port = find_free_port()
    if not port:
        click.echo("Error: 无法找到可用端口")
        return

    click.echo(f"正在分析项目: {project_root}")
    click.echo(f"Web界面启动在: http://127.0.0.1:{port}")

    # 在后台启动项目分析
    tools = ProjectTools(project_root=project_root)
    tools.start_monitoring()

    # 设置环境变量
    os.environ["PROJECT_ROOT"] = project_root

    # 启动 Web 服务，关闭热重载和访问日志
    uvicorn.run(
        "ohmyprompt.web.app:app",
        host="127.0.0.1",
        port=port,
        reload=False,  # 关闭热重载
        access_log=False,  # 关闭访问日志
        log_level="error",  # 只显示错误日志
    )


def main():
    """CLI入口函数"""
    cli()


if __name__ == "__main__":
    main()
