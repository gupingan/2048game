import sys
from PyQt5.QtWidgets import QApplication
from Model.model import Model
from View.view import GameView

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = Model()
    view = GameView(model)
    view.show()
    sys.exit(app.exec_())
