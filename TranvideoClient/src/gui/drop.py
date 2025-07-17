from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os


class DropWidget(QWidget):
    files_dropped = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setMinimumHeight(120)
        self.setStyleSheet("""
            DropWidget {
                border: 2px dashed #aaa;
                border-radius: 8px;
                background-color: #f8f8f8;
            }
            DropWidget:hover {
                border-color: #4CAF50;
                background-color: #f0f8f0;
            }
        """)

        # 布局和标签
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # 图标
        icon_label = QLabel("📁")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 32px; border: none; background: transparent;")

        # 文字说明
        text_label = QLabel("拖拽MP4视频文件到此区域\n或点击上方选择文件")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("color: #666; border: none; background: transparent;")

        layout.addWidget(icon_label)
        layout.addWidget(text_label)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            valid_files = []
            for url in urls:
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if os.path.isfile(file_path) and file_path.lower().endswith('.mp4'):
                        valid_files.append(file_path)

            if valid_files:
                event.acceptProposedAction()
                self.setStyleSheet("""
                    DropWidget {
                        border: 2px dashed #4CAF50;
                        border-radius: 8px;
                        background-color: #e8f5e8;
                    }
                """)
            else:
                event.ignore()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            DropWidget {
                border: 2px dashed #aaa;
                border-radius: 8px;
                background-color: #f8f8f8;
            }
            DropWidget:hover {
                border-color: #4CAF50;
                background-color: #f0f8f0;
            }
        """)

    def dropEvent(self, event):
        files = []
        for url in event.mimeData().urls():
            if url.isLocalFile():
                file_path = url.toLocalFile()
                if os.path.isfile(file_path) and file_path.lower().endswith('.mp4'):
                    files.append(file_path)

        if files:
            self.files_dropped.emit(files)
            event.acceptProposedAction()

        # 恢复样式
        self.dragLeaveEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)