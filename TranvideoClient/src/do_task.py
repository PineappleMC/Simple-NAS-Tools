import os
import subprocess
import json
import tempfile
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
import configparser


class TaskProcessor:
    def __init__(self, ffmpeg_path: str = "src/ffmpeg.exe"):
        self.ffmpeg_path = ffmpeg_path
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.config_path = Path("config/app.config")
        self.config_path.parent.mkdir(exist_ok=True)

    def get_video_duration(self, video_path: str) -> Optional[float]:
        """获取视频时长"""
        try:
            cmd = [
                self.ffmpeg_path, "-i", video_path, "-hide_banner",
                "-f", "null", "-", "-v", "quiet", "-show_entries",
                "format=duration", "-of", "csv=p=0"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return float(result.stdout.strip())
        except:
            pass

        # 备用方案：使用ffprobe
        try:
            cmd = [
                self.ffmpeg_path.replace("ffmpeg", "ffprobe"), "-v", "quiet",
                "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
                video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return float(result.stdout.strip())
        except:
            pass

        return None

    def create_white_video(self, duration: float, output_path: str) -> bool:
        """生成白色视频"""
        try:
            cmd = [
                self.ffmpeg_path, "-f", "lavfi", "-i", f"color=white:size=320x240:duration={duration}",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "30",
                "-y", output_path
            ]
            result = subprocess.run(cmd, capture_output=True)
            return result.returncode == 0
        except:
            return False

    def extract_audio(self, video_path: str, audio_path: str) -> bool:
        """提取音频"""
        try:
            cmd = [
                self.ffmpeg_path, "-i", video_path, "-vn", "-acodec", "copy",
                "-y", audio_path
            ]
            result = subprocess.run(cmd, capture_output=True)
            return result.returncode == 0
        except:
            return False

    def merge_audio_video(self, video_path: str, audio_path: str, output_path: str) -> bool:
        """合并音视频"""
        try:
            cmd = [
                self.ffmpeg_path, "-i", video_path, "-i", audio_path,
                "-c:v", "copy", "-c:a", "aac", "-shortest", "-y", output_path
            ]
            result = subprocess.run(cmd, capture_output=True)
            return result.returncode == 0
        except:
            return False

    def process_video_for_upload(self, video_path: str) -> Optional[str]:
        """处理视频用于上传"""
        video_name = Path(video_path).stem
        duration = self.get_video_duration(video_path)
        if not duration:
            return None

        # 生成缓存文件路径
        white_video = self.cache_dir / f"{video_name}_white.mp4"
        audio_file = self.cache_dir / f"{video_name}_audio.aac"
        output_file = self.cache_dir / f"{video_name}_processed.mp4"

        # 创建白色视频
        if not self.create_white_video(duration, str(white_video)):
            return None

        # 提取音频
        if not self.extract_audio(video_path, str(audio_file)):
            return None

        # 合并音频和白色视频
        if not self.merge_audio_video(str(white_video), str(audio_file), str(output_file)):
            return None

        # 清理临时文件
        white_video.unlink(missing_ok=True)
        audio_file.unlink(missing_ok=True)

        return str(output_file)

    def add_soft_subtitle(self, video_path: str, srt_path: str, output_path: str) -> bool:
        """添加软字幕"""
        try:
            cmd = [
                self.ffmpeg_path, "-i", video_path, "-i", srt_path,
                "-c:v", "copy", "-c:a", "copy", "-c:s", "srt",
                "-disposition:s:0", "default", "-y", output_path
            ]
            result = subprocess.run(cmd, capture_output=True)
            return result.returncode == 0
        except:
            return False

    def save_task_config(self, task_data: Dict[str, Any]) -> None:
        """保存任务配置"""
        config = configparser.ConfigParser()
        if self.config_path.exists():
            config.read(self.config_path)

        if not config.has_section('tasks'):
            config.add_section('tasks')

        config.set('tasks', 'pending_tasks', json.dumps(task_data))

        with open(self.config_path, 'w') as f:
            config.write(f)

    def load_task_config(self) -> Dict[str, Any]:
        """加载任务配置"""
        if not self.config_path.exists():
            return {}

        config = configparser.ConfigParser()
        config.read(self.config_path)

        if config.has_option('tasks', 'pending_tasks'):
            try:
                return json.loads(config.get('tasks', 'pending_tasks'))
            except:
                return {}
        return {}

    def clear_pending_tasks(self) -> None:
        """清理待处理任务"""
        config = configparser.ConfigParser()
        if self.config_path.exists():
            config.read(self.config_path)

        if config.has_section('tasks'):
            config.remove_option('tasks', 'pending_tasks')

        with open(self.config_path, 'w') as f:
            config.write(f)

    def cleanup_cache(self) -> None:
        """清理缓存目录"""
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(exist_ok=True)