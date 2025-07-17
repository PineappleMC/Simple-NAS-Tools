#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.gui import MainWindow
from src import APIClient, TaskProcessor


def check_dependencies():
    """检查必要的依赖"""
    missing = []

    # 检查ffmpeg
    ffmpeg_path = "src/ffmpeg.exe"
    if not os.path.exists(ffmpeg_path):
        missing.append("ffmpeg.exe 未找到")

    # 检查配置目录
    config_dir = "config"
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    # 检查缓存目录
    cache_dir = "cache"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    return missing


def main():
    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName("视频字幕处理客户端")
    app.setApplicationVersion("1.0.0")

    # 设置应用属性
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # 检查依赖
    missing_deps = check_dependencies()
    if missing_deps:
        QMessageBox.critical(
            None, "依赖检查失败",
            "缺少必要文件:\n" + "\n".join(missing_deps)
        )
        return 1

    try:
        # 创建主窗口
        window = MainWindow()
        window.show()

        # 运行应用
        return app.exec_()

    except Exception as e:
        QMessageBox.critical(
            None, "启动错误",
            f"程序启动失败:\n{str(e)}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())