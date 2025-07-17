#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息显示模块 - 负责聊天界面的渲染和消息展示
"""

import tkinter as tk
from tkinter import ttk
import datetime


class MessageDisplay:
    def __init__(self, parent):
        self.parent = parent

    def setup_ui(self, row, columnspan):
        """设置UI"""
        # 对话显示区域
        self.chat_frame = ttk.LabelFrame(
            self.parent,
            text="对话内容",
            padding="10"
        )
        self.chat_frame.grid(
            row=row,
            column=0,
            columnspan=columnspan,
            sticky=(tk.W, tk.E, tk.N, tk.S),
            pady=(0, 10)
        )
        self.chat_frame.columnconfigure(0, weight=1)
        self.chat_frame.rowconfigure(0, weight=1)

        # 创建聊天显示区域
        self.chat_display = tk.Text(
            self.chat_frame,
            height=20,
            width=80,
            state=tk.DISABLED,
            wrap=tk.WORD,
            font=("Arial", 10),
            bg="#f8f9fa",
            relief=tk.FLAT
        )

        # 滚动条
        scrollbar = ttk.Scrollbar(
            self.chat_frame,
            orient=tk.VERTICAL,
            command=self.chat_display.yview
        )
        self.chat_display.configure(yscrollcommand=scrollbar.set)

        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # 配置聊天样式
        self.setup_chat_styles()

    def setup_chat_styles(self):
        """设置聊天样式"""
        # 模型A消息样式 - 左对齐，蓝色背景
        self.chat_display.tag_config("model_a_bubble",
                                     background="#007acc",
                                     foreground="white",
                                     font=("Arial", 12),
                                     relief=tk.SOLID,
                                     borderwidth=0,
                                     wrap=tk.WORD,
                                     lmargin1=20,
                                     lmargin2=20,
                                     rmargin=100)

        # 模型B消息样式 - 右对齐，深绿色背景
        self.chat_display.tag_config("model_b_bubble",
                                     background="#128c7e",
                                     foreground="white",
                                     font=("Arial", 12),
                                     relief=tk.SOLID,
                                     borderwidth=0,
                                     wrap=tk.WORD,
                                     lmargin1=100,
                                     lmargin2=100,
                                     rmargin=20)

        # 时间戳样式
        self.chat_display.tag_config("timestamp",
                                     foreground="#666666",
                                     font=("Arial", 8),
                                     justify=tk.CENTER)

        # 系统消息样式
        self.chat_display.tag_config("system",
                                     foreground="#999999",
                                     font=("Arial", 9, "italic"),
                                     justify=tk.CENTER)

        # 用户名样式
        self.chat_display.tag_config("username_a",
                                     foreground="#007acc",
                                     font=("Arial", 9, "bold"))

        self.chat_display.tag_config("username_b",
                                     foreground="#128c7e",
                                     font=("Arial", 9, "bold"))

    def append_message(self, message, model, round_num):
        """以聊天气泡形式添加消息"""
        self.chat_display.config(state=tk.NORMAL)

        # 添加时间戳
        timestamp = datetime.datetime.now().strftime("%H:%M")

        # 添加用户名和时间
        if model == "A":
            self.chat_display.insert(tk.END, f"模型A  {timestamp}\n", "username_a")
        else:
            self.chat_display.insert(tk.END, f"模型B  {timestamp}\n", "username_b")

        # 添加消息内容
        message_tag = f"model_{model.lower()}_bubble"

        # 分割长消息为多行
        lines = message.split('\n')
        for i, line in enumerate(lines):
            if line.strip():  # 只处理非空行
                # 每行添加一些内边距
                padded_line = f"  {line.strip()}  "
                self.chat_display.insert(tk.END, padded_line, message_tag)
                if i < len(lines) - 1:
                    self.chat_display.insert(tk.END, "\n", message_tag)

        # 添加换行分隔
        self.chat_display.insert(tk.END, "\n\n\n")

        # 滚动到底部
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def add_system_message(self, message):
        """添加系统消息"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"--- {message} ---\n", "system")
        self.chat_display.insert(tk.END, "\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def clear_chat(self):
        """清空聊天内容"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)