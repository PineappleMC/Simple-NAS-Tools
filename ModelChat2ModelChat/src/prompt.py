#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提示词管理模块 - 负责提示词输入、保存和加载
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os


class PromptManager:
    def __init__(self, parent):
        self.parent = parent
        self.config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config',
            'prompt_memory.json'
        )
        self.load_prompts()

    def setup_ui(self, row, columnspan):
        """设置UI"""
        # 提示词输入框架
        self.prompt_frame = ttk.LabelFrame(
            self.parent,
            text="初始提示词设置",
            padding="10"
        )
        self.prompt_frame.grid(
            row=row,
            column=0,
            columnspan=columnspan,
            sticky=(tk.W, tk.E),
            pady=(0, 10)
        )
        self.prompt_frame.columnconfigure(0, weight=1)
        self.prompt_frame.columnconfigure(1, weight=1)

        # 模型A提示词
        ttk.Label(
            self.prompt_frame,
            text="模型A初始提示词:"
        ).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))

        self.prompt_a = scrolledtext.ScrolledText(
            self.prompt_frame,
            height=3,
            width=40,
            font=("Arial", 10)
        )
        self.prompt_a.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 5))

        # 模型B提示词
        ttk.Label(
            self.prompt_frame,
            text="模型B初始提示词:"
        ).grid(row=0, column=1, sticky=tk.W, padx=(5, 0))

        self.prompt_b = scrolledtext.ScrolledText(
            self.prompt_frame,
            height=3,
            width=40,
            font=("Arial", 10)
        )
        self.prompt_b.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))

        # 按钮框架
        button_frame = ttk.Frame(self.prompt_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # 保存按钮
        ttk.Button(
            button_frame,
            text="保存提示词",
            command=self.save_prompts
        ).grid(row=0, column=0, padx=(0, 5))

        # 重置按钮
        ttk.Button(
            button_frame,
            text="重置为默认",
            command=self.reset_prompts
        ).grid(row=0, column=1, padx=(0, 5))

        # 加载保存的提示词
        self.load_saved_prompts_to_ui()

    def load_prompts(self):
        """从配置文件加载提示词"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.prompts = json.load(f)
        except FileNotFoundError:
            # 默认提示词
            self.prompts = {
                "model_a": "你是一个友好的AI助手，请开始对话。",
                "model_b": "你是一个有创造力的AI助手，请参与对话。"
            }
            self.save_prompts_to_file()

    def load_saved_prompts_to_ui(self):
        """将保存的提示词加载到UI"""
        self.prompt_a.delete("1.0", tk.END)
        self.prompt_a.insert(tk.END, self.prompts["model_a"])

        self.prompt_b.delete("1.0", tk.END)
        self.prompt_b.insert(tk.END, self.prompts["model_b"])

    def save_prompts(self):
        """保存当前提示词"""
        self.prompts["model_a"] = self.prompt_a.get("1.0", tk.END).strip()
        self.prompts["model_b"] = self.prompt_b.get("1.0", tk.END).strip()

        if self.save_prompts_to_file():
            messagebox.showinfo("成功", "提示词已保存")

    def save_prompts_to_file(self):
        """保存提示词到文件"""
        try:
            config_dir = os.path.dirname(self.config_path)
            os.makedirs(config_dir, exist_ok=True)

            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.prompts, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {e}")
            return False

    def reset_prompts(self):
        """重置为默认提示词"""
        self.prompts = {
            "model_a": "你是一个友好的AI助手，请开始对话。",
            "model_b": "你是一个有创造力的AI助手，请参与对话。"
        }
        self.load_saved_prompts_to_ui()

    def get_prompt_a(self):
        """获取模型A提示词"""
        return self.prompt_a.get("1.0", tk.END).strip()

    def get_prompt_b(self):
        """获取模型B提示词"""
        return self.prompt_b.get("1.0", tk.END).strip()

    def validate_prompts(self):
        """验证提示词是否有效"""
        prompt_a = self.get_prompt_a()
        prompt_b = self.get_prompt_b()

        if not prompt_a or not prompt_b:
            messagebox.showwarning("警告", "请先设置两个模型的初始提示词")
            return False
        return True