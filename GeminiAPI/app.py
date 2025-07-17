import requests
import json
import time


class GeminiChatbot:
    def __init__(self, api_key, model="gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def chat(self, prompt, retry_on_quota=True):
        """发送消息到Gemini API"""
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"

        headers = {
            'Content-Type': 'application/json',
        }

        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }

        try:
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    return result['candidates'][0]['content']['parts'][0]['text']
                else:
                    return "抱歉，没有收到有效回复"

            elif response.status_code == 429 and retry_on_quota:
                # 处理配额限制
                error_info = response.json()
                retry_delay = 60  # 默认等待时间

                # 尝试从错误信息中获取建议的重试时间
                if 'error' in error_info and 'details' in error_info['error']:
                    for detail in error_info['error']['details']:
                        if detail.get('@type') == 'type.googleapis.com/google.rpc.RetryInfo':
                            retry_delay = int(detail.get('retryDelay', '60s').rstrip('s'))
                            break

                print(f"遇到配额限制，等待 {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
                return self.chat(prompt, retry_on_quota=False)  # 重试一次

            else:
                error_info = response.json() if response.content else {}
                return f"API错误 ({response.status_code}): {error_info.get('error', {}).get('message', '未知错误')}"

        except Exception as e:
            return f"请求异常: {str(e)}"

    def chat_loop(self):
        """交互式聊天循环"""
        print(f"🤖 Gemini聊天机器人已启动 (使用模型: {self.model})")
        print("输入 'quit'、'exit' 或 'bye' 退出聊天")
        print("-" * 50)

        while True:
            try:
                user_input = input("\n你: ").strip()

                if user_input.lower() in ['quit', 'exit', 'bye', '退出']:
                    print("👋 再见！")
                    break

                if not user_input:
                    continue

                print("🤖 Gemini: ", end="", flush=True)
                response = self.chat(user_input)
                print(response)

            except KeyboardInterrupt:
                print("\n\n👋 聊天已结束！")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {e}")


# 使用示例
if __name__ == "__main__":
    API_KEY = "AIzaSyCcW7Q3z-gXtObuMgzBjC5UFlaS6luGS2c"

    # 创建聊天机器人实例
    chatbot = GeminiChatbot(API_KEY, model="gemini-2.0-flash")

    # 单次对话示例
    print("=== 单次对话测试 ===")
    response = chatbot.chat("用一句话介绍一下人工智能")
    print(f"回答: {response}")

    print("\n=== 进入交互模式 ===")
    # 开始交互式聊天
    chatbot.chat_loop()