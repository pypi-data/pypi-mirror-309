#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# DevVersion: Python3.6.8
# Date: 2020-09-25 09:13
# PyCharm|setup

from setuptools import (setup, find_packages)

setup(
    # 包名
    name="MyBpm",
    # 版本
    version="0.1",
    # 包的解释地址
    # long_description=open('ReadMe.md', encoding='utf-8').read(),
    # 需要包含的子包列表
    packages=find_packages()
)
