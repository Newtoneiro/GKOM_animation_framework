from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtCore import QTimer

from src.graphics_engine import GraphicsEngine
from src.window.gui import GUI
from src.window.gui_animation import GUIAnimation
from src.constants import (
    WINDOW_CONSTANTS,
    GE_WIDGET_CONSTANTS,
    GUI_WIDGET_CONSTANTS,
    GUI_ANIMATION_WIDGET_CONSTANTS,
)


class MainWindow(QMainWindow):
    """
    Class for the main window.
    """

    def __init__(self):
        super(MainWindow, self).__init__()

        self._init_window()
        self._init_central_widget()
        self._init_ge_widget()
        self._init_gui_widget()
        self._init_gui_animation_widget()

        self._init_timer()

    def _init_window(self) -> None:
        """
        Initializes the window.
        """
        screen_geometry = QApplication.desktop().screenGeometry()

        window_width = WINDOW_CONSTANTS.WIDTH
        window_height = WINDOW_CONSTANTS.HEIGHT
        window_x = (screen_geometry.width() - window_width) // 2
        window_y = (screen_geometry.height() - window_height) // 2

        self.setGeometry(window_x, window_y, window_width, window_height)
        self.setWindowTitle("Graphics Engine")
        self.layout = QVBoxLayout()
        self.sublayout = QHBoxLayout()
        self.layout.addLayout(self.sublayout)

    def _init_central_widget(self) -> None:
        """
        Initializes the central widget.
        """
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def _init_ge_widget(self) -> None:
        """
        Initializes the widget.
        """
        self.ge_widget = GraphicsEngine()
        self.ge_widget.setFixedWidth(GE_WIDGET_CONSTANTS.WIDTH)
        self.ge_widget.setFixedHeight(GE_WIDGET_CONSTANTS.HEIGHT)
        self.sublayout.addWidget(self.ge_widget)

    def _init_gui_widget(self) -> None:
        """
        Initializes the widget.
        """
        self.gui_widget = GUI(self.ge_widget)
        self.gui_widget.setFixedWidth(GUI_WIDGET_CONSTANTS.WIDTH)
        self.sublayout.addWidget(self.gui_widget)

    def _init_gui_animation_widget(self) -> None:
        """
        Initializes the widget
        """
        self.gui_animation_widget = GUIAnimation(self.gui_widget)
        self.gui_animation_widget.setFixedHeight(
            GUI_ANIMATION_WIDGET_CONSTANTS.HEIGHT
        )
        self.layout.addWidget(self.gui_animation_widget)

    def _init_timer(self) -> None:
        """
        Initializes the timer.
        """
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.ge_widget.update)
        self.timer.timeout.connect(self.gui_widget.update)
        self.timer.start(GE_WIDGET_CONSTANTS.TIME_PER_TICK)
