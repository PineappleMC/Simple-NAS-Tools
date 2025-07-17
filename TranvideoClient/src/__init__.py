"""
视频字幕处理客户端
"""

from .use_api import APIClient
from .do_task import TaskProcessor

__version__ = "1.0.0"
__author__ = "Video Subtitle Client"

__all__ = ["APIClient", "TaskProcessor"]