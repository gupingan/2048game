"""
block.py
==========

Block类是2048游戏中的方块类，用于表示游戏中的方块，它包含以下功能：

在构造函数中，创建一个QLabel对象作为子窗口，并设置其大小和对齐方式，用于显示方块上的文本。
定义一个QPoint类型的私有属性 _grid_pos，用于保存方块在游戏棋盘上的坐标。

- set_label: 用于设置方块上的文本。
- set_style_sheet: 用于设置方块的样式表。
- slide: 用于在棋盘上滑动方块，并实现了动画效果。
- create_block，用于创建一个方块对象，设置方块上的文本和位置，并返回创建的方块对象。

Author: 顾初见（Ronan Gu） <ronangu@foxmail.com>

Date: 2023-4-5
"""
from PyQt5.QtCore import QPropertyAnimation, QPoint, Qt, pyqtProperty
from PyQt5.QtWidgets import QWidget, QLabel


class Block(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = QLabel(self)  # 创建一个QLabel对象，并将其作为子窗口添加到Block对象中
        self.label.setFixedSize(100, 100)  # 设置QLabel的固定大小为100x100
        self.label.setAlignment(Qt.AlignCenter)  # 设置QLabel的文本居中对齐
        self.animation = None  # 创建一个QPropertyAnimation动画对象，并将其初始化为None
        self._grid_pos = QPoint()  # 创建一个QPoint对象，用于保存方块在游戏棋盘上的坐标

    def set_label(self, value):
        self.label.setText(str(value))  # 设置QLabel的文本为value

    def set_style_sheet(self, style_sheet):
        self.label.setStyleSheet(style_sheet)  # 设置QLabel的样式表

    @pyqtProperty(QPoint)
    def grid_pos(self):
        return self._grid_pos  # 返回方块在游戏棋盘上的坐标

    @grid_pos.setter
    def grid_pos(self, pos):
        self._grid_pos = pos
        self.move(pos.x() * self.width(), pos.y() * self.height())  # 移动方块到棋盘上的指定位置

    def slide(self, target_pos):
        """
        暂时废弃，方块滑动方法
        :param target_pos: 移动目标坐标，使用QPoint传入
        :return:
        """
        if self.animation and self.animation.state() == QPropertyAnimation.Running:
            self.animation.stop()  # 如果动画正在运行，则停止动画
        self.animation = QPropertyAnimation(self, b"grid_pos", self)  # 创建一个QPropertyAnimation动画对象
        self.animation.setEndValue(target_pos)  # 设置动画的结束位置
        self.animation.setDuration(500)  # 设置动画的持续时间为500ms
        self.animation.start()  # 启动动画

    @staticmethod
    def create_block(value, pos: QPoint):
        """
        实例化对象
        :param value: 方块上的文本
        :param pos: 位置
        :return: Block 该类的一个实例对象
        """
        block = Block()  # 创建一个Block对象
        block.set_label(value)  # 设置方块的文本为value
        block.grid_pos = pos  # 设置方块在游戏棋盘上的位置
        return block  # 返回创建的方块对象
