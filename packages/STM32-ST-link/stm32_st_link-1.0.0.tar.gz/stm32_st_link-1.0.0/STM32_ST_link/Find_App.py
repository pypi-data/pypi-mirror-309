#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/14 上午9:30
# @Author  : 周梦泽
# @File    : Find_App.py
# @Software: PyCharm
# @Description:查找应用程序的路径

import winreg
import os
import subprocess
from typing import List


def find_software_path(software_name: str) -> List[str]:
    """
    查找Windows系统中指定软件的安装路径

    Args:
        software_name: 要查找的软件名称

    Returns:
        包含所有找到的安装路径的列表
    """
    paths = []

    # 1. 通过注册表查找
    def check_registry_key(key_path: str) -> None:
        try:
            # 打开注册表键
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)

            # 遍历所有子键
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)

                    try:
                        # 尝试读取安装路径
                        install_path = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                        display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]

                        if software_name.lower() in display_name.lower() and install_path:
                            if os.path.exists(install_path):
                                paths.append(install_path)

                    except (WindowsError, KeyError):
                        pass
                    finally:
                        winreg.CloseKey(subkey)
                    i += 1
                except WindowsError:
                    break
            winreg.CloseKey(key)
        except WindowsError:
            pass

    # 检查常见的注册表路径
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for reg_path in registry_paths:
        check_registry_key(reg_path)

    # 2. 在常见安装目录中搜索
    common_paths = [
        os.environ.get("ProgramFiles", "C:\\Program Files"),
        os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
    ]

    for base_path in common_paths:
        if os.path.exists(base_path):
            for root, dirs, files in os.walk(base_path):
                if software_name.lower() in root.lower():
                    paths.append(root)

    # 3. 使用 where 命令查找可执行文件
    try:
        result = subprocess.run(['where', f'{software_name}.exe'],
                                capture_output=True,
                                text=True)
        if result.returncode == 0:
            paths.extend(result.stdout.splitlines())
    except subprocess.SubprocessError:
        pass

    return list(set(paths))  # 去重返回


# 使用示例
if __name__ == "__main__":
    # software_name = input("请输入要查找的软件名称: ")

    paths = find_software_path("STM32 ST-LINK Utility")

    if paths:
        print("\n找到以下安装路径:")
        for path in paths:
            print(f"- {path}")
    else:
        print("未找到相关安装路径")
