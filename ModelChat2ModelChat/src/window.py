#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口模块 - 负责整体UI布局和组件集成
"""

import tkinter as tk
from tkinter import ttk
import json
import os

from prompt import PromptManager
from messages_show import MessageDisplay
from button import ButtonController
from logic import ConversationLogic


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.load_config()
        self.init_components()
        self.setup_layout()

    def setup_window(self):
        """设置窗口基本属性"""
        self.root.title("Ollama模型对话程序")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def load_config(self):
        """加载配置文件"""
        config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')

        # 加载API配置
        api_config_path = os.path.join(config_dir, 'ollama_api.json')
        try:
            with open(api_config_path, 'r', encoding='utf-8') as f:
                self.api_config = json.load(f)
        except FileNotFoundError:
            # 默认配置
            self.api_config = {
                "url": "http://192.168.9.120:11434",
                "model": "qwq:32b",
                "timeout": 60
            }
            self.save_api_config()

    def save_api_config(self):
        """保存API配置"""
        config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
        os.makedirs(config_dir, exist_ok=True)

        api_config_path = os.path.join(config_dir, 'ollama_api.json')
        with open(api_config_path, 'w', encoding='utf-8') as f:
            json.dump(self.api_config, f, ensure_ascii=False, indent=2)

    def init_components(self):
        """初始化各个组件"""
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")

        # 初始化各个功能模块
        self.prompt_manager = PromptManager(self.main_frame)
        self.message_display = MessageDisplay(self.main_frame)
        self.conversation_logic = ConversationLogic(
            self.api_config,
            self.message_display
        )
        self.button_controller = ButtonController(
            self.main_frame,
            self.conversation_logic,
            self.prompt_manager,
            self.message_display
        )

    def setup_layout(self):
        """设置布局"""
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)

        # 标题
        title_label = ttk.Label(
            self.main_frame,
            text="Ollama模型对话程序",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # 提示词管理器
        self.prompt_manager.setup_ui(row=1, columnspan=2)

        # 消息显示区域
        self.message_display.setup_ui(row=2, columnspan=2)

        # 按钮控制器
        self.button_controller.setup_ui(row=3, columnspan=2)

        # 状态栏
        self.status_label = ttk.Label(self.main_frame, text="状态: 就绪")
        self.status_label.grid(row=4, column=0, columnspan=2, sticky=tk.W)

        # 设置状态更新回调
        self.conversation_logic.set_status_callback(self.update_status)

    def update_status(self, message):
        """更新状态显示"""
        self.status_label.config(text=f"状态: {message}")

    def get_api_config(self):
        """获取API配置"""
        return self.api_config