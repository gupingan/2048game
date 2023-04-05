"""
message_box.py
==========

继承自QMessageBox的自定义类，用于创建一个带有“确认”和“取消”按钮的消息框。
它可以接收自定义的标题和文本内容，以及在点击按钮时执行的回调函数，用于在2048游戏中实现胜利或失败后的弹窗。
当用户点击“确认”或“取消”按钮时，该类会检查按钮的角色并调用相应的回调函数。
如果用户点击了消息框的关闭按钮，则会执行取消回调函数。`

Author: 顾初见（Ronan Gu） <ronangu@foxmail.com>

Date: 2023-4-5
"""
import sys

from PyQt5.QtWidgets import QMessageBox, QApplication


class GameMessageBox(QMessageBox):
    def __init__(self, title, text, on_ok_clicked=None, on_cancel_clicked=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_ok_clicked = on_ok_clicked  # 当点击“确认”按钮时要执行的回调函数
        self.on_cancel_clicked = on_cancel_clicked  # 当点击“取消”按钮时要执行的回调函数
        self.setWindowTitle(title)  # 设置窗口标题
        self.setText(text)  # 设置显示的文本内容
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  # 设置标准的“确认”和“取消”按钮

        if on_ok_clicked:
            self.buttonClicked.connect(lambda button: self._handle_ok_clicked(button, self.on_ok_clicked))

        if on_cancel_clicked:
            self.buttonClicked.connect(lambda button: self._handle_cancel_clicked(button, self.on_cancel_clicked))

    def _handle_ok_clicked(self, button, callback):
        if self.buttonRole(button) == QMessageBox.AcceptRole:  # 判断点击的按钮是“确认”按钮
            callback()
        else:
            self.close()

    def _handle_cancel_clicked(self, button, callback):
        if self.buttonRole(button) == QMessageBox.RejectRole:  # 判断点击的按钮是“取消”按钮
            callback()
        else:
            self.close()

    def closeEvent(self, event):
        if event.spontaneous():  # 检查事件是否不是通过调用close()函数引起的
            self.on_cancel_clicked()  # 执行取消回调函数

        super().closeEvent(event)


# 代码测试用
if __name__ == '__main__':
    app = QApplication(sys.argv)
    box = GameMessageBox("Game", "TEST")
    box.show()
    sys.exit(app.exec_())
