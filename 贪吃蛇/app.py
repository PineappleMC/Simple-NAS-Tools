import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer, Qt, QRect
from PyQt5.QtGui import QPainter, QColor

class SnakeGame(QWidget):
    def __init__(self, cell_size=20, window_size=(400, 400)):
        super().__init__()
        self.setWindowTitle("PyQt 贪吃蛇游戏")
        self.cell_size = cell_size
        self.resize(*window_size)
        self.init_game()

    def init_game(self):
        # 根据窗口大小动态计算网格范围
        self.grid_width = self.width() // self.cell_size
        self.grid_height = self.height() // self.cell_size

        # 初始蛇的位置居中
        center_x = self.grid_width // 2
        center_y = self.grid_height // 2
        self.snake = [
            (center_x - 1, center_y),
            (center_x, center_y),
            (center_x + 1, center_y)
        ]
        self.direction = (0, 1)  # 初始向下
        self.food = self.generate_food()
        self.score = 0

        # 定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)  # 调整速度

    def paintEvent(self, event):
        qp = QPainter(self)
        self.draw_grid(qp)
        self.draw_snake(qp)
        self.draw_food(qp)

    def draw_grid(self, qp):
        pen = qp.pen()
        pen.setWidth(1)
        qp.setPen(pen)
        for x in range(0, self.width(), self.cell_size):
            qp.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), self.cell_size):
            qp.drawLine(0, y, self.width(), y)

    def draw_snake(self, qp):
        qp.setBrush(Qt.green)
        for x, y in self.snake:
            rect = QRect(x * self.cell_size, y * self.cell_size,
                         self.cell_size, self.cell_size)
            qp.drawRect(rect)

    def draw_food(self, qp):
        qp.setBrush(Qt.red)
        x, y = self.food
        rect = QRect(x * self.cell_size, y * self.cell_size,
                     self.cell_size, self.cell_size)
        qp.drawRect(rect)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up and self.direction != (0, 1):
            self.direction = (0, -1)
        elif key == Qt.Key_Down and self.direction != (0, -1):
            self.direction = (0, 1)
        elif key == Qt.Key_Left and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif key == Qt.Key_Right and self.direction != (-1, 0):
            self.direction = (1, 0)

    def generate_food(self):
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def update(self):
        # 移动蛇
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # 检查碰撞
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or
            new_head[1] < 0 or new_head[1] >= self.grid_height or
            new_head in self.snake[:-1]):
            self.game_over()
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

        self.repaint()

    def game_over(self):
        self.timer.stop()
        # 可以添加重置游戏的逻辑
        print("Game Over! Score:", self.score)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 调整参数控制网格大小和窗口尺寸
    game = SnakeGame(cell_size=25, window_size=(800, 600))  # 示例：25x25网格，800x600窗口
    game.show()
    sys.exit(app.exec_())