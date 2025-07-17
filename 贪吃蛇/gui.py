# gui.py
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QFont


class GameView(QWidget):
    def __init__(self):
        super().__init__()
        self.cell_size = 20  # 每个网格的像素大小
        self.grid_width = 20  # 网格总列数
        self.grid_height = 20  # 网格总行数
        self.snake_body = []  # 蛇的身体坐标列表
        self.food_position = (0, 0)  # 食物坐标
        self.score = 0  # 当前得分
        self.game_over = False  # 是否游戏结束

    def set_initial_state(self, state):
        """设置初始游戏状态"""
        self.snake_body = state['snake']
        self.food_position = state['food']
        self.score = state['score']
        self.grid_width = state['grid_width']
        self.grid_height = state['grid_height']
        self.update()  # 强制刷新界面

    def update_view(self, new_state):
        """接收游戏逻辑更新并刷新界面"""
        self.snake_body = new_state['snake']
        self.food_position = new_state['food']
        self.score = new_state['score']
        self.update()  # 触发重绘

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制网格背景
        self.draw_grid(painter)

        # 绘制蛇
        self.draw_snake(painter)

        # 绘制食物
        self.draw_food(painter)

        # 显示得分
        self.draw_score(painter)

        # 游戏结束时显示信息
        if self.game_over:
            self.draw_game_over(painter)

    def draw_grid(self, painter):
        """绘制网格线"""
        painter.setPen(QColor(100, 100, 100))
        for x in range(self.grid_width):
            painter.drawLine(x * self.cell_size, 0,
                             x * self.cell_size, self.height())
        for y in range(self.grid_height):
            painter.drawLine(0, y * self.cell_size,
                             self.width(), y * self.cell_size)

    def draw_snake(self, painter):
        """绘制蛇的身体"""
        painter.setBrush(QColor(0, 255, 0))  # 绿色
        for pos in self.snake_body:
            x, y = pos
            rect = (x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size)
            painter.drawRect(*rect)

    def draw_food(self, painter):
        """绘制食物"""
        painter.setBrush(QColor(255, 0, 0))  # 红色
        x, y = self.food_position
        rect = (x * self.cell_size,
                y * self.cell_size,
                self.cell_size,
                self.cell_size)
        painter.drawRect(*rect)

    def draw_score(self, painter):
        """显示得分"""
        painter.setPen(Qt.black)
        painter.setFont(QFont('Arial', 12))
        painter.drawText(10, 20, f"得分: {self.score}")

    def draw_game_over(self, painter):
        """显示游戏结束信息"""
        painter.setPen(Qt.red)
        painter.setFont(QFont('Arial', 20))
        text = "游戏结束！"
        rect = painter.boundingRect(0, 0, self.width(), self.height(), Qt.AlignCenter, text)
        painter.drawText(rect, Qt.AlignCenter, text)

    def show_game_over_message(self):
        """标记游戏结束状态"""
        self.game_over = True
        self.update()