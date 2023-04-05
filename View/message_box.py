import sys

from PyQt5.QtWidgets import QMessageBox, QApplication


class GameMessageBox(QMessageBox):
    def __init__(self, title, text, on_ok_clicked=None, on_cancel_clicked=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_ok_clicked = on_ok_clicked
        self.on_cancel_clicked = on_cancel_clicked
        self.setWindowTitle(title)
        self.setText(text)
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # self.finished.connect(self.on_cancel_clicked)

        if on_ok_clicked:
            self.buttonClicked.connect(lambda button: self._handle_ok_clicked(button, self.on_ok_clicked))

        if on_cancel_clicked:
            self.buttonClicked.connect(lambda button: self._handle_cancel_clicked(button, self.on_cancel_clicked))

    def _handle_ok_clicked(self, button, callback):
        if self.buttonRole(button) == QMessageBox.AcceptRole:
            callback()
        else:
            self.close()

    def _handle_cancel_clicked(self, button, callback):
        if self.buttonRole(button) == QMessageBox.RejectRole:
            callback()
        else:
            self.close()

    def closeEvent(self, event):
        if event.spontaneous():  # Check if the event is not caused by a call to the close() function
            self.on_cancel_clicked()

        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    box = GameMessageBox("Game", "TEST")
    box.show()
    sys.exit(app.exec_())
