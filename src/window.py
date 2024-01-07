from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import Qt, QTimer
from src.graphics_engine import GraphicsEngine

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setGeometry(100, 100, 1600, 900)

        self.central_widget = GraphicsEngine()
        self.setCentralWidget(self.central_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.central_widget.update)
        self.timer.start(10)