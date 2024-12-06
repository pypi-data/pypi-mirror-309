#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/19 下午1:49
# @Author  : 周梦泽
# @File    : setup.py
# @Software: PyCharm
# @Description:定义了你的包的元数据

from setuptools import setup, find_packages

setup(
    name="STM32_ST-link",  # 包名，PyPI 上唯一
    version="1.0.0",  # 版本号
    author="Mason Zhou",  # 作者名
    author_email="qq2087698086@gmail.com",  # 作者邮箱
    description="STM32 ST-Link CLI microcontroller operations: connect, program, and erase. Before use, STM32 ST-LINK "
                "Utility must be installed.",  # 简短描述

    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="",  # 项目主页
    packages=find_packages(),  # 自动找到包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
