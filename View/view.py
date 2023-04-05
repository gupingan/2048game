"""
view.py
==========

该文件包含GameView类，主要作用有：

- 显示游戏区块、分数标签和按钮等元素；
- 更新游戏区块的显示和分数标签，并在游戏胜利或失败时弹出消息框；
- 设置游戏界面的样式，包括背景颜色、分数标签和游戏区块的样式；
- 处理用户的按键事件，以控制游戏的运行。
除此之外，GameView类还持有一个Model对象，用于与游戏模型进行交互，实现游戏的逻辑。

Author: 顾初见（Ronan Gu） <ronangu@foxmail.com>

Date: 2023-4-5
"""
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, \
    QMessageBox
from PyQt5.QtGui import QKeyEvent, QPalette, QColor, QFont
from PyQt5.QtCore import Qt, QEvent, QPoint
# 导入自定义的Model类、GameMessageBox类和Block类。
from Model.model import Model
from View.message_box import GameMessageBox
from View.block import Block


class GameView(QWidget):
    def __init__(self, model: Model):
        super().__init__()
        self.model = model
        self.block_movement_flag = True  # 新增一个标志位来控制方块的移动
        self.setWindowTitle("2048-GAME")
        # 创建两个QLabel对象来显示当前分数和最高分数。
        self.score_label = QLabel(f"当前分数: {self.model.score}")
        self.score_label.setFont(QFont("Arial", 16))
        self.score_label.setAlignment(Qt.AlignCenter)
        self.highest_score_label = QLabel(f"最高分数: {self.model.highest_score}")
        self.highest_score_label.setFont(QFont("Arial", 16))
        self.highest_score_label.setAlignment(Qt.AlignCenter)
        # 创建一个QGridLayout对象，用于管理16个Block对象，设置Block之间的垂直和水平间距为10。
        self.grid_layout = QGridLayout()
        self.grid_layout.setVerticalSpacing(10)
        self.grid_layout.setHorizontalSpacing(10)
        # 创建两个QPushButton对象，分别用于重新开始和退出游戏，并为它们的点击事件绑定对应的槽函数。
        self.new_game_button = QPushButton("重新开始")
        self.new_game_button.setFixedSize(100, 40)
        self.new_game_button.setFont(QFont("Arial", 14))
        self.new_game_button.clicked.connect(self.new_game_button_clicked)
        self.quit_button = QPushButton("退出游戏")
        self.quit_button.setFixedSize(100, 40)
        self.quit_button.setFont(QFont("Arial", 14))
        self.quit_button.clicked.connect(self.quit_button_clicked)
        # 创建一个水平的QHBoxLayout对象，用于存放重新开始和退出游戏的QPushButton对象，并设置它们之间的间距为20
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.new_game_button)
        hbox_layout.addWidget(self.quit_button)
        hbox_layout.setContentsMargins(0, 20, 0, 0)
        hbox_layout.setSpacing(20)
        hbox_layout.setAlignment(Qt.AlignCenter)
        # 创建一个水平的QHBoxLayout对象，用于存放当前分数和最高分数的QLabel对象，并设置它们之间的间距为20。
        score_layout = QHBoxLayout()
        score_layout.addWidget(self.score_label)
        score_layout.addWidget(self.highest_score_label)
        score_layout.setAlignment(Qt.AlignCenter)
        score_layout.setSpacing(20)
        score_layout.setContentsMargins(5, 5, 5, 5)
        # 创建一个垂直的QVBoxLayout对象，用于存放当前分数和最高分数
        vbox_layout = QVBoxLayout()
        vbox_layout.addLayout(score_layout)
        vbox_layout.addLayout(self.grid_layout)
        vbox_layout.addLayout(hbox_layout)
        vbox_layout.setContentsMargins(10, 10, 10, 10)
        vbox_layout.addStretch()
        # 更改焦点
        self.setFocusPolicy(Qt.StrongFocus)
        self.setLayout(vbox_layout)
        # 设置样式
        self.set_style()

    def set_style(self):
        """
        初始化设置游戏界面的样式，包括背景颜色、分数标签和游戏区块的样式
        :return:
        """
        # 设置背景颜色
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#faf8ef"))  # 设置颜色为浅黄色
        self.setAutoFillBackground(True)  # 设置自动填充背景
        self.setPalette(palette)  # 设置背景调色板
        # # 设置分数标签的样式
        self.score_label.setStyleSheet("""
            color: #776e65;
        """)
        self.highest_score_label.setStyleSheet("""
            color: #776e65;
        """)
        # 设置游戏区块的样式
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

    def update_view(self):
        """
        更新游戏区块的显示和分数标签，并在游戏胜利或失败时弹出消息框
        :return:
        """
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

        # 更新分数标签
        self.score_label.setText(f"当前分数: {self.model.score}")
        self.highest_score_label.setText(f"最高分数: {self.model.highest_score}")

    def block_not_movement(self):
        """
        设置标志位以禁止游戏区块的移动
        :return:
        """
        self.block_movement_flag = False

    def load_highest_score(self):
        """
        View层加载最高分数并在界面上显示
        :return:
        """
        self.model.load_highest_score()
        self.highest_score_label.setText(f"最高分数: {self.model.highest_score}")

    def showEvent(self, event) -> None:
        """
        窗口显示事件，当窗口被打开时执行
        获取自适应后的长宽，设置为窗口的固定大小，并初始化游戏
        :param event:
        :return:
        """
        super().showEvent(event)
        # 获取自适应后的长宽
        width = self.sizeHint().width()
        height = self.sizeHint().height()
        # 设置固定大小
        self.setFixedSize(width, height)

        self.new_game_button_clicked()

    def event(self, event: QEvent):
        """
        判断当前事件是否是应用程序激活事件，如果是则加载之前保存的最高分
        :param event:
        :return:
        """
        if event.type() == QEvent.ApplicationActivate:
            self.load_highest_score()
        return super().event(event)

    def keyPressEvent(self, event: QKeyEvent):
        """
        键盘按下事件处理方法，根据按下的键调用相应的移动方法，并调用update_view方法更新界面
        :param event:
        :return:
        """
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
        """
        窗口关闭事件处理方法，如果当前分数不是最高分数，则保存最高分数
        :param event:
        :return:
        """
        if self.model.highest_score >= self.model.score:
            self.model.save_highest_score()
        event.accept()

    def new_game_button_clicked(self):
        """
        点击新游戏按钮事件处理方法，重置游戏数据，更新视图，将焦点设置在窗口上，并设置游戏焦点为第一个方块
        :return:
        """
        self.block_movement_flag = True
        self.model.reset()
        self.update_view()
        self.setFocus()
        self.setTabOrder(self, self.grid_layout.itemAt(0).widget())

    def quit_button_clicked(self):
        """
        响应退出按钮点击事件
        :return:
        """
        reply = QMessageBox.question(self, "退出游戏", "你想要退出游戏2048吗?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

    @staticmethod
    def get_color(value):
        """
        定义一个字典，存储数字和对应颜色
        :param value: int 方块上的数字
        :return:
        """
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
        return colors.get(value, "#CDC1B4")  # 如果字典中存在该数字，则返回对应颜色，否则返回默认颜色

    @staticmethod
    def get_font_size(value):
        """
        根据数字大小返回不同字体大小
        :param value: int 方块上的数字
        :return: int 字体大小
        """
        if value < 100:
            return 36
        elif value < 1000:
            return 32
        else:
            return 24


# 代码测试
if __name__ == '__main__':
    pass
