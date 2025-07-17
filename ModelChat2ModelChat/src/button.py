#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按钮控制模块 - 负责按钮UI和事件处理
"""

import tkinter as tk
from tkinter import ttk


class ButtonController:
    def __init__(self, parent, conversation_logic, prompt_manager, message_display):
        self.parent = parent
        self.conversation_logic = conversation_logic
        self.prompt_manager = prompt_manager
        self.message_display = message_display

    def setup_ui(self, row, columnspan):
        """设置按钮UI"""
        # 控制按钮框架
        self.control_frame = ttk.Frame(self.parent)
        self.control_frame.grid(row=row, column=0, columnspan=columnspan, pady=(0, 10))

        # 开始对话按钮
        self.start_button = ttk.Button(
            self.control_frame,
            text="开始对话",
            command=self.start_conversation
        )
        self.start_button.grid(row=0, column=0, padx=(0, 5))

        # 停止对话按钮
        self.stop_button = ttk.Button(
            self.control_frame,
            text="停止对话",
            command=self.stop_conversation,
            state=tk.DISABLED
        )
        self.stop_button.grid(row=0, column=1, padx=(0, 5))

        # 清空对话按钮
        self.clear_button = ttk.Button(
            self.control_frame,
            text="清空对话",
            command=self.clear_conversation
        )
        self.clear_button.grid(row=0, column=2, padx=(0, 5))

    def start_conversation(self):
        """开始对话处理"""
        # 验证提示词
        if not self.prompt_manager.validate_prompts():
            return

        # 更新按钮状态
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # 获取提示词
        prompt_a = self.prompt_manager.get_prompt_a()
        prompt_b = self.prompt_manager.get_prompt_b()

        # 添加开始消息
        self.message_display.add_system_message("对话开始")

        # 启动对话逻辑
        self.conversation_logic.start_conversation(prompt_a, prompt_b)

    def stop_conversation(self):
        """停止对话处理"""
        # 停止对话逻辑
        self.conversation_logic.stop_conversation()

        # 更新按钮状态
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def clear_conversation(self):
        """清空对话处理"""
        # 清空消息显示
        self.message_display.clear_chat()

        # 清空对话历史
        self.conversation_logic.clear_history()

    def set_buttons_enabled(self, enabled):
        """设置按钮启用状态"""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.start_button.config(state=state)
        self.clear_button.config(state=state)