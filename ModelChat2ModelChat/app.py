#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama模型对话程序 - 主入口
Author: Assistant
Date: 2025
"""

import tkinter as tk
import sys
import os

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from window import MainWindow


def main():
    """主函数"""
    try:
        # 创建主窗口
        root = tk.Tk()

        # 创建应用实例
        app = MainWindow(root)

        # 启动事件循环
        root.mainloop()

    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"程序启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()