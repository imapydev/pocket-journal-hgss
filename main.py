import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout
)


class App(QMainWindow):

    def __init__(self):
        super().__init__()

        self.master_canvas = QWidget()
        self.master_layout = QVBoxLayout()

        self.master_canvas.setLayout(self.master_layout)
        self.setCentralWidget(self.master_canvas)
        self.show()


app = QApplication(sys.argv)
window = App()
app.exec()