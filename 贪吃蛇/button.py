from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication


class KeyHandler(QObject):
    direction_changed = pyqtSignal(tuple)  # 发射新的方向信号

    def __init__(self):
        super().__init__()
        self.direction = (0, 1)  # 初始方向（右）
        self.install_event_filter()

    def install_event_filter(self):
        """将事件过滤器安装到应用程序"""
        app = QApplication.instance()
        app.installEventFilter(self)

    def eventFilter(self, obj, event):
        """监听键盘事件"""
        if event.type() == Qt.KeyPress:
            key = event.key()
            new_dir = None

            if key == Qt.Key_Up or key == Qt.Key_W:
                new_dir = (0, -1)
            elif key == Qt.Key_Down or key == Qt.Key_S:
                new_dir = (0, 1)
            elif key == Qt.Key_Left or key == Qt.Key_A:
                new_dir = (-1, 0)
            elif key == Qt.Key_Right or key == Qt.Key_D:
                new_dir = (1, 0)

            if new_dir:
                self.direction = new_dir
                self.direction_changed.emit(new_dir)

        return super().eventFilter(obj, event)