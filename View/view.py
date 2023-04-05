from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, \
    QMessageBox
from PyQt5.QtGui import QKeyEvent, QPalette, QColor, QFont
from PyQt5.QtCore import Qt, QEvent, QPoint
import sys
from Model.model import Model
from View.message_box import GameMessageBox
from View.block import Block


class GameView(QWidget):
    def __init__(self, model: Model):
        super().__init__()

        self.model = model
        self.block_movement_flag = True  # 新增一个标志位来控制方块的移动

        self.setWindowTitle("2048-GAME")
        # self.setFixedSize(500, 580)

        # Create the score label and center it
        self.score_label = QLabel(f"当前分数: {self.model.score}")
        self.score_label.setFont(QFont("Arial", 16))
        self.score_label.setAlignment(Qt.AlignCenter)

        # Create the highest score label and center it
        self.highest_score_label = QLabel(f"最高分数: {self.model.highest_score}")
        self.highest_score_label.setFont(QFont("Arial", 16))
        self.highest_score_label.setAlignment(Qt.AlignCenter)

        # Create the grid layout
        self.grid_layout = QGridLayout()
        self.grid_layout.setVerticalSpacing(10)
        self.grid_layout.setHorizontalSpacing(10)
        # self.grid_layout.setAlignment(Qt.AlignCenter)

        # Add the new game and quit buttons
        self.new_game_button = QPushButton("重新开始")
        self.new_game_button.setFixedSize(100, 40)
        self.new_game_button.setFont(QFont("Arial", 14))
        self.new_game_button.clicked.connect(self.new_game_button_clicked)

        self.quit_button = QPushButton("退出游戏")
        self.quit_button.setFixedSize(100, 40)
        self.quit_button.setFont(QFont("Arial", 14))
        self.quit_button.clicked.connect(self.quit_button_clicked)

        # Create a horizontal layout for the new game and quit buttons
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.new_game_button)
        hbox_layout.addWidget(self.quit_button)
        hbox_layout.setContentsMargins(0, 20, 0, 0)
        hbox_layout.setSpacing(20)
        hbox_layout.setAlignment(Qt.AlignCenter)

        # Add the score label and highest_score to a horizontal layout
        score_layout = QHBoxLayout()
        score_layout.addWidget(self.score_label)
        score_layout.addWidget(self.highest_score_label)
        score_layout.setAlignment(Qt.AlignCenter)
        score_layout.setSpacing(20)
        score_layout.setContentsMargins(5, 5, 5, 5)

        # Add the score horizontal layout, grid layout, and buttons to a vertical layout
        vbox_layout = QVBoxLayout()
        vbox_layout.addLayout(score_layout)
        vbox_layout.addLayout(self.grid_layout)
        vbox_layout.addLayout(hbox_layout)
        vbox_layout.setContentsMargins(10, 10, 10, 10)
        vbox_layout.addStretch()

        # Set the focus policy and layout
        self.setFocusPolicy(Qt.StrongFocus)
        self.setLayout(vbox_layout)

        self.set_style()

    def set_style(self):
        # Set background color
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#faf8ef"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Set style for score label
        self.score_label.setStyleSheet("""
            color: #776e65;
        """)

        self.highest_score_label.setStyleSheet("""
            color: #776e65;
        """)

        # Set style for grid
        for i in range(4):
            for j in range(4):
                block = Block.create_block(" ", QPoint(i, j))
                block.setFixedSize(100, 100)
                block.set_style_sheet("""
                    background-color: #cdc1b4;
                    border-radius: 6px;
                    color: #776e65;
                """)
                self.grid_layout.addWidget(block, i, j)
                # label = QLabel(" ")
                # label.setAlignment(Qt.AlignCenter)
                # label.setFixedSize(100, 100)
                # label.setStyleSheet("""
                #     background-color: #cdc1b4;
                #     border-radius: 6px;
                #     color: #776e65;
                # """)
                # self.grid_layout.addWidget(label, i, j)

    def update_view(self):
        print("update_view 被调用")
        # print(self.model.last_move_direction)
        # Update grid
        for i in range(4):
            for j in range(4):
                value = self.model.grid[i][j]
                block = self.grid_layout.itemAtPosition(i, j).widget()
                if isinstance(block, Block):
                    if self.model.last_move_direction == "left":
                        pass
                    elif self.model.last_move_direction == "right":
                        pass
                    elif self.model.last_move_direction == "up":
                        pass
                    elif self.model.last_move_direction == "down":
                        pass
                    else:
                        pass
                    block.set_label(str(value) if value != 0 else " ")
                    block.set_style_sheet(f"""
                        background-color: {self.get_color(value)};
                        border-radius: 6px;
                        color: {'#f9f6f2' if value in [2, 4] else '#776e65'};
                        font-size: {self.get_font_size(value)}px;
                    """)

        if self.model.check_win():
            win = GameMessageBox("你赢了！", "本场对局你已胜利，点击确定后重新开始！",
                                 self.new_game_button_clicked, self.block_not_movement)
            win.show()

        if self.model.check_lost():
            lost = GameMessageBox("你输啦！", "本局游戏已失败，点击确定后重新开始！",
                                  self.new_game_button_clicked, self.block_not_movement)
            lost.show()

        # Update score label
        self.score_label.setText(f"当前分数: {self.model.score}")
        self.highest_score_label.setText(f"最高分数: {self.model.highest_score}")

    def block_not_movement(self):
        self.block_movement_flag = False

    def load_highest_score(self):
        self.model.load_highest_score()
        self.highest_score_label.setText(f"最高分数: {self.model.highest_score}")

    def showEvent(self, event) -> None:
        super().showEvent(event)

        # 获取自适应后的长宽
        width = self.sizeHint().width()
        height = self.sizeHint().height()

        # 设置固定大小
        self.setFixedSize(width, height)

        self.new_game_button_clicked()

    def event(self, event: QEvent):
        if event.type() == QEvent.ApplicationActivate:
            self.load_highest_score()
        return super().event(event)

    def keyPressEvent(self, event: QKeyEvent):
        if self.block_movement_flag:
            if event.key() == Qt.Key_Up:
                self.model.move_up()
            elif event.key() == Qt.Key_Down:
                self.model.move_down()
            elif event.key() == Qt.Key_Left:
                self.model.move_left()
            elif event.key() == Qt.Key_Right:
                self.model.move_right()
        self.update_view()

    def closeEvent(self, event):
        if self.model.highest_score >= self.model.score:
            self.model.save_highest_score()
        event.accept()

    def new_game_button_clicked(self):
        self.block_movement_flag = True
        self.model.reset()
        self.update_view()
        self.setFocus()
        self.setTabOrder(self, self.grid_layout.itemAt(0).widget())  # 恢复游戏焦点

    def quit_button_clicked(self):
        reply = QMessageBox.question(self, "退出游戏", "你想要退出游戏2048吗?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

    @staticmethod
    def get_color(value):
        colors = {
            2: "#FFDAB9",  # 浅杏仁色
            4: "#FFA07A",  # 海洋红色
            8: "#FF7F50",  # 珊瑚橙色
            16: "#FF6347",  # 番茄红色
            32: "#FF4500",  # 橙红色
            64: "#FF8C00",  # 暗橙色
            128: "#FFFF00",  # 鲜黄色
            256: "#FFD700",  # 金色
            512: "#FFA500",  # 橙色
            1024: "#FF8F00",  # 暗橙色
            2048: "#FF4500"  # 橙红色
        }
        return colors.get(value, "#CDC1B4")

    @staticmethod
    def get_font_size(value):
        if value < 100:
            return 36
        elif value < 1000:
            return 32
        else:
            return 24


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_model = Model()
    view = GameView(game_model)
    view.show()
    sys.exit(app.exec_())
