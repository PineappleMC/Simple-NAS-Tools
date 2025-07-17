# window.py
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from gui import GameView
from action import GameLogic
from button import KeyHandler


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("贪吃蛇游戏")
        self.setGeometry(100, 100, 400, 400)

        # 初始化核心模块
        self.game_view = GameView()
        self.game_logic = GameLogic()
        self.key_handler = KeyHandler(self)

        # 布局设置
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.game_view)

        # 信号与槽的连接
        self.key_handler.direction_changed.connect(self.game_logic.set_direction)
        self.game_logic.game_state_updated.connect(self.game_view.update_view)
        self.game_logic.game_over_signal.connect(self.show_game_over)

        # 初始化游戏
        self.game_logic.start_new_game()
        self.game_view.set_initial_state(self.game_logic.get_state())

        # 启动游戏循环
        self.timer = self.game_logic.get_timer()
        self.timer.start(150)  # 默认帧率（可配置）

    def keyPressEvent(self, event):
        self.key_handler.handle_key(event)

    def show_game_over(self):
        self.timer.stop()
        self.game_view.show_game_over_message()
        # 可添加重置按钮或提示
        print("游戏结束！最终得分：", self.game_logic.score)

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()