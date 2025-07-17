#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话逻辑模块 - 负责对话流程控制和状态管理
"""

import threading
import time
from ollama_api import OllamaAPI


class ConversationLogic:
    def __init__(self, config, message_display):
        self.config = config
        self.message_display = message_display
        self.ollama_api = OllamaAPI(config)

        # 对话状态
        self.is_running = False
        self.conversation_history = []
        self.status_callback = None

        # 配置参数
        self.max_rounds = config.get("max_rounds", 20)
        self.delay_between_requests = config.get("delay_between_requests", 2)

    def set_status_callback(self, callback):
        """设置状态更新回调"""
        self.status_callback = callback

    def update_status(self, message):
        """更新状态"""
        if self.status_callback:
            self.status_callback(message)

    def start_conversation(self, prompt_a, prompt_b):
        """开始对话"""
        self.is_running = True
        self.conversation_history = []

        # 在新线程中运行对话
        thread = threading.Thread(
            target=self.run_conversation,
            args=(prompt_a, prompt_b)
        )
        thread.daemon = True
        thread.start()

    def stop_conversation(self):
        """停止对话"""
        self.is_running = False
        self.update_status("对话已停止")

    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
        self.update_status("对话历史已清空")

    def run_conversation(self, prompt_a, prompt_b):
        """运行对话循环"""
        try:
            # 第一轮：模型A开始
            current_prompt = prompt_a
            current_model = "A"
            round_count = 1

            while self.is_running and round_count <= self.max_rounds:
                self.update_status(f"第{round_count}轮 - 模型{current_model}思考中...")

                # 调用API
                response = self.ollama_api.call_api(current_prompt)

                if not self.is_running:
                    break

                # 检查是否有错误
                if response.startswith(("连接错误", "请求超时", "API调用错误", "未知错误")):
                    self.message_display.add_system_message(f"错误: {response}")
                    self.update_status(f"错误: {response}")
                    break

                # 显示对话
                self.message_display.append_message(response, current_model, round_count)

                # 保存到历史
                self.conversation_history.append({
                    "round": round_count,
                    "model": current_model,
                    "prompt": current_prompt,
                    "response": response
                })

                # 切换模型和准备下一轮提示词
                if current_model == "A":
                    current_model = "B"
                    # 如果是第一轮，使用模型B的初始提示词 + 模型A的回应
                    if round_count == 1:
                        current_prompt = f"{prompt_b}\n\n对方说：{response}"
                    else:
                        current_prompt = response
                else:
                    current_model = "A"
                    current_prompt = response

                round_count += 1

                # 添加延迟避免过快请求
                if self.is_running:
                    time.sleep(self.delay_between_requests)

            if self.is_running:
                self.update_status("对话完成")
                self.message_display.add_system_message("对话已完成")

        except Exception as e:
            error_msg = f"对话过程中发生错误: {str(e)}"
            self.message_display.add_system_message(error_msg)
            self.update_status(error_msg)
        finally:
            self.is_running = False

    def get_conversation_history(self):
        """获取对话历史"""
        return self.conversation_history

    def export_conversation(self, file_path):
        """导出对话历史"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("Ollama模型对话记录\n")
                f.write("=" * 50 + "\n\n")

                for item in self.conversation_history:
                    f.write(f"第{item['round']}轮 - 模型{item['model']}\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"{item['response']}\n\n")

            return True
        except Exception as e:
            return False, str(e)