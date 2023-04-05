"""
main.py
==========

2048游戏入口

Author: 顾初见（Ronan Gu） <ronangu@foxmail.com>

Date: 2023-4-5
"""
import sys
from PyQt5.QtWidgets import QApplication
from Model.model import Model
from View.view import GameView

# 游戏入口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = Model()
    view = GameView(model)
    view.show()
    sys.exit(app.exec_())
