from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import random


class GameLogic(QObject):
    game_state_updated = pyqtSignal(dict)
    game_over_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.grid_size = (20, 20)  # 网格尺寸（列，行）
        self.snake = [(5, 5), (5, 4), (5, 3)]  # 初始蛇身坐标（头在第一个元素）
        self.direction = (0, 1)  # 初始方向（右）
        self.food = self.generate_food()  # 初始食物位置
        self.score = 0
        self.game_over = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)

    def start_new_game(self):
        self.__init__()  # 重置所有属性
        self.timer.start(150)  # 默认150ms（约6.6帧/秒）

    def update_game(self):
        # 计算新头部位置
        new_head = (
            self.snake[0][0] + self.direction[0],
            self.snake[0][1] + self.direction[1]
        )

        # 边界碰撞检测
        if (new_head[0] < 0 or new_head[0] >= self.grid_size[0] or
                new_head[1] < 0 or new_head[1] >= self.grid_size[1]):
            self.game_over = True
            self.game_over_signal.emit()
            return

        # 自身碰撞检测（排除尾部）
        if new_head in self.snake[:-1]:
            self.game_over = True
            self.game_over_signal.emit()
            return

        # 移动蛇：添加新头，判断是否吃食物
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()  # 生成新食物
        else:
            self.snake.pop()  # 移除尾部

        # 发射状态更新信号
        self.game_state_updated.emit(self.get_state())

    def generate_food(self):
        while True:
            x = random.randint(0, self.grid_size[0] - 1)
            y = random.randint(0, self.grid_size[1] - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def set_direction(self, new_dir):
        # 防止反向移动（如当前向右不能立即左转）
        opposite = (-new_dir[0], -new_dir[1])
        if self.direction != opposite:
            self.direction = new_dir

    def get_state(self):
        return {
            'snake': self.snake.copy(),
            'food': self.food,
            'score': self.score,
            'grid_width': self.grid_size[0],
            'grid_height': self.grid_size[1]
        }

    def get_timer(self):
        return self.timer