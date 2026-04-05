"""
AviationAI - 民航航务大模型安装脚本
"""
from setuptools import setup, find_packages

setup(
    name="aviation-ai",
    version="0.1.0",
    description="基于AI的民航航务智能监控系统",
    author="璇玑史CEO",
    packages=find_packages(),
    install_requires=[
        "flask>=2.0",
        "sqlite3",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "aviation-ai=gui.dashboard:main",
        ],
    },
)
