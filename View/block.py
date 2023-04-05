from PyQt5.QtCore import QPropertyAnimation, QPoint, Qt, pyqtProperty
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel


class Block(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = QLabel(self)
        self.label.setFixedSize(100, 100)
        self.label.setAlignment(Qt.AlignCenter)
        self.animation = None  # 添加这行代码
        self._grid_pos = QPoint()

    def set_label(self, value):
        self.label.setText(str(value))

    def set_style_sheet(self, style_sheet):
        self.label.setStyleSheet(style_sheet)

    @pyqtProperty(QPoint)
    def grid_pos(self):
        return self._grid_pos

    @grid_pos.setter
    def grid_pos(self, pos):
        self._grid_pos = pos
        self.move(pos.x() * self.width(), pos.y() * self.height())

    def slide(self, target_pos):
        if self.animation and self.animation.state() == QPropertyAnimation.Running:
            self.animation.stop()
        self.animation = QPropertyAnimation(self, b"grid_pos", self)
        self.animation.setEndValue(target_pos)
        self.animation.setDuration(500)
        self.animation.start()

    @staticmethod
    def create_block(value, pos: QPoint):
        block = Block()
        block.set_label(value)
        block.grid_pos = pos
        return block
