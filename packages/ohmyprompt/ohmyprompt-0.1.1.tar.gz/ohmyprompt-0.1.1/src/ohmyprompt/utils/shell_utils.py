import subprocess


def execute_bash(command: str, timeout: int = 30) -> tuple[str, str, int]:
    """
    安全地执行shell命令

    Args:
        command: 要执行的命令
        timeout: 超时时间(秒)

    Returns:
        tuple: (stdout, stderr, return_code)
    """
    try:
        # 使用 shell=True 来执行完整的命令字符串
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,  # 使用 shell 执行命令
            executable="/bin/bash",  # 指定使用 bash
        )
        stdout, stderr = process.communicate(timeout=timeout)
        return stdout, stderr, process.returncode
    except subprocess.TimeoutExpired:
        process.kill()
        return "", "命令执行超时", 1
    except Exception as e:
        return "", str(e), 1
