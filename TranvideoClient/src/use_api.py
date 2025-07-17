import requests
import json
import os
import time
from typing import Optional, Dict, Any


class APIClient:
    def __init__(self, base_url: str, invite_code: str):
        self.base_url = base_url.rstrip('/')
        self.invite_code = invite_code
        self.session = requests.Session()
        self.session.timeout = 30

    def check_invitation(self) -> Dict[str, Any]:
        """验证邀请码"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/invitation/check/{self.invite_code}"
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"valid": False, "error": str(e)}

    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        try:
            response = self.session.get(f"{self.base_url}/api/status")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"busy": True, "queue_length": 0, "error": str(e)}

    def check_whisper_health(self) -> Dict[str, Any]:
        """检查Whisper服务健康状态"""
        try:
            response = self.session.get(f"{self.base_url}/api/whisper/health")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"available": False, "error": str(e)}

    def upload_for_srt(self, file_path: str) -> Dict[str, Any]:
        """上传单个视频文件生成字幕"""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f, 'video/mp4')}
                response = self.session.post(
                    f"{self.base_url}/api/process/srt/{self.invite_code}",
                    files=files
                )
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        except FileNotFoundError:
            return {"error": f"文件不存在: {file_path}"}

    def batch_upload_for_srt(self, file_paths: list) -> Dict[str, Any]:
        """批量上传视频文件生成字幕"""
        try:
            files = []
            for file_path in file_paths:
                files.append(('files', (os.path.basename(file_path),
                                        open(file_path, 'rb'), 'video/mp4')))

            data = {'mode': 'srt'}
            response = self.session.post(
                f"{self.base_url}/api/batch/process/{self.invite_code}",
                files=files,
                data=data
            )
            response.raise_for_status()

            # 关闭文件句柄
            for _, file_tuple in files:
                file_tuple[1].close()

            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """查询单个任务状态"""
        try:
            response = self.session.get(f"{self.base_url}/api/task/{task_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": str(e)}

    def get_batch_status(self, batch_id: str) -> Dict[str, Any]:
        """查询批量任务状态"""
        try:
            response = self.session.get(f"{self.base_url}/api/batch/{batch_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": str(e)}

    def download_srt(self, filename: str, save_path: str) -> bool:
        """下载SRT字幕文件"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/download/srt/{filename}",
                stream=True
            )
            response.raise_for_status()

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except requests.exceptions.RequestException as e:
            print(f"下载失败: {e}")
            return False
        except Exception as e:
            print(f"保存失败: {e}")
            return False

    def download_batch_zip(self, batch_id: str, save_path: str) -> bool:
        """下载批量任务的压缩包"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/batch/download/{batch_id}",
                stream=True
            )
            response.raise_for_status()

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except requests.exceptions.RequestException as e:
            print(f"下载失败: {e}")
            return False
        except Exception as e:
            print(f"保存失败: {e}")
            return False