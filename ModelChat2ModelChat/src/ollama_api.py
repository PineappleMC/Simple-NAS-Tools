#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama API接口模块 - 负责与Ollama服务的通信
"""

import requests
import json
import re


class OllamaAPI:
    def __init__(self, config):
        self.url = config.get("url", "http://localhost:11434")
        self.model = config.get("model", "qwq:32b")
        self.timeout = config.get("timeout", 600)
        self.stream = config.get("stream", False)

    def remove_think_tags(self, text):
        """移除<think>标签及其内容"""
        pattern = r'<think>.*?</think>'
        cleaned_text = re.sub(pattern, '', text, flags=re.DOTALL)
        return cleaned_text.strip()

    def call_api(self, prompt):
        """调用Ollama API"""
        try:
            url = f"{self.url}/api/generate"
            data = {
                "model": self.model,
                "prompt": prompt,
                "stream": self.stream
            }

            response = requests.post(url, json=data, timeout=self.timeout)
            response.raise_for_status()

            result = response.json()
            raw_response = result.get("response", "")

            # 移除思考标签
            cleaned_response = self.remove_think_tags(raw_response)
            return cleaned_response

        except requests.exceptions.ConnectionError:
            return "连接错误: 无法连接到Ollama服务"
        except requests.exceptions.Timeout:
            return "请求超时: Ollama服务响应太慢"
        except requests.exceptions.RequestException as e:
            return f"API调用错误: {str(e)}"
        except json.JSONDecodeError:
            return "API返回格式错误"
        except Exception as e:
            return f"未知错误: {str(e)}"

    def test_connection(self):
        """测试连接"""
        try:
            url = f"{self.url}/api/tags"
            response = requests.get(url, timeout=50)
            response.raise_for_status()
            return True, "连接成功"
        except Exception as e:
            return False, f"连接失败: {str(e)}"