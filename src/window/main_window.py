from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer

from src.graphics_engine import GraphicsEngine
from src.constants import WINDOW_CONSTANTS


class MainWindow(QMainWindow):
    """
    Class for the main window.
    """
    def __init__(self):
        super(MainWindow, self).__init__()

        self._init_window()
        self._init_widget()
        self._init_timer()

    def _init_window(self):
        """
        Initializes the window.
        """
        screen_geometry = QApplication.desktop().screenGeometry()

        window_width = WINDOW_CONSTANTS.WIDTH
        window_height = WINDOW_CONSTANTS.HEIGHT
        window_x = (screen_geometry.width() - window_width) // 2
        window_y = (screen_geometry.height() - window_height) // 2

        self.setGeometry(window_x, window_y, window_width, window_height)

    def _init_widget(self):
        """
        Initializes the widget.
        """
        self.central_widget = GraphicsEngine()
        self.setCentralWidget(self.central_widget)

    def _init_timer(self):
        """
        Initializes the timer.
        """
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.central_widget.update)
        self.timer.start(10)
