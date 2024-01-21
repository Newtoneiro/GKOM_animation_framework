import cv2
import numpy as np

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QWidget, QSlider, QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QPainter, QBrush, QColor, QPaintEvent
from collections import defaultdict

from src.window.gui import GUI
from src.constants import GUI_ANIMATION_WIDGET_CONSTANTS

def calculate_new_vector_linear(
        prev: tuple,
        next: tuple,
        cframe: int
        ) -> tuple:
    """
    Calculates the new vector based on the previous and
    next vector and the current frame.

    :param prev: The previous vector.
    :param next: The next vector.
    :param cframe: The current frame.
    """
    pframe, (px, py, pz) = prev
    nframe, (nx, ny, nz) = next
    x = px + (nx - px) * ((cframe - pframe) / (nframe - pframe))
    y = py + (ny - py) * ((cframe - pframe) / (nframe - pframe))
    z = pz + (nz - pz) * ((cframe - pframe) / (nframe - pframe))
    return x, y, z


class MarkerSlider(QSlider):
    """
    A slider that can have markers on it.
    """
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setMaximum(200)

        self.markers = set()

    def add_marker(self) -> None:
        """
        Adds a marker to the slider.
        """
        value = self.value()
        self.markers.add(value)
        self.update()

    def value_to_pos(self, value: int) -> int:
        """
        Converts a value to a position on the slider.

        :param value: The value to convert.
        """
        return (value / self.maximum()) * (self.width() - 12) + 6

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Paints the markers on the slider.

        :param event: The paint event.
        """
        super().paintEvent(event)
        painter = QPainter(self)
        for value in self.markers:
            pos = self.value_to_pos(value)
            self.draw_marker(painter, pos)

    def draw_marker(self, painter: QPainter, pos: int) -> None:
        """
        Draws a marker on the slider.

        :param painter: The painter.
        :param pos: The position of the marker.
        """
        marker_width = 4
        marker_height = self.height()
        rect = QRectF(pos - marker_width / 2, 0, marker_width, marker_height)
        painter.fillRect(rect, QBrush(QColor("red")))


class GUIAnimation(QWidget):
    """
    The GUI for the animation.
    """
    def __init__(self, gui: GUI):
        super(GUIAnimation, self).__init__()

        self.layout = QGridLayout(self)
        self.gui = gui
        self.key_frames = defaultdict(dict)
        self._init_slider()
        self._init_buttons()
        self.frame_label = QLabel(f"Frame: {self.slider.value()}")
        self.layout.addWidget(self.frame_label, 0, 1, 2, 1)

    def _slider_value_update(self, value: int) -> None:
        """
        Updates the frame label.

        :param value: The value of the slider.
        """
        self.frame_label.setText(f"Frame: {value}")
        self.update_objects(value)

    def _init_slider(self) -> None:
        """
        Initializes the slider.
        """
        self.slider = MarkerSlider(Qt.Orientation.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self._slider_value_update)

        self.layout.addWidget(self.slider, 0, 0, 2, 1)
        self.slider.add_marker()

    def _init_buttons(self) -> None:
        """
        Initializes the buttons.
        """
        self.addKeyFrameButton = QPushButton("Add key")
        self.addKeyFrameButton.clicked.connect(
            self._on_add_keyframe_button_clicked
        )
        self.layout.addWidget(self.addKeyFrameButton, 0, 2, 1, 1)

        self.renderButton = QPushButton("Render")
        self.renderButton.clicked.connect(self._on_render_button_clicked)
        self.layout.addWidget(self.renderButton, 0, 3, 1, 1)

    def _on_add_keyframe_button_clicked(self, _) -> None:
        """
        Adds a keyframe to the selected object.
        """
        if self.gui.selected_object is None:
            return

        frame = self.slider.value()
        self.slider.add_marker()
        obj = self.gui.selected_object
        self.key_frames[obj._name][frame] = (obj._pos, obj._rot, obj._scale)

    def _on_render_button_clicked(self, _) -> None:
        """
        Renders the animation.
        """
        img = self.gui.ge.grabFrameBuffer()
        img = img.convertToFormat(4)
        width, height = img.width(), img.height()
        result = cv2.VideoWriter(
            f"{GUI_ANIMATION_WIDGET_CONSTANTS.OUTPUT_FILE_NAME}.avi",
            cv2.VideoWriter_fourcc(*"MJPG"),
            GUI_ANIMATION_WIDGET_CONSTANTS.OUTPUT_FPS,
            (
                width,
                height
            )
        )
        for i in range(self.slider.minimum(), self.slider.maximum() + 1):
            self.update_objects(i)
            self.gui.ge.update()
            self.gui.ge.paintGL()
            img = self.gui.ge.grabFrameBuffer()
            img = img.convertToFormat(4)

            ptr = img.bits()
            ptr.setsize(img.byteCount())
            img = np.array(ptr, np.uint8).reshape(height, width, 4)
            img = img[:, :, 0:3]
            result.write(img)
        pass
        result.release()

    def update_objects(self, frame: int) -> None:
        """
        Updates the objects to the given frame.

        :param frame: The frame to update to.
        """
        for obj_name, keyframes in self.key_frames.items():
            obj = next(
                (o for o in self.gui.ge._scene if obj_name == o._name),
                None
            )
            if obj is not None:
                if frame in keyframes:
                    pos, rot, scale = keyframes[frame]
                    obj._pos = pos
                    obj._rot = rot
                    obj._scale = scale
                elif len(keyframes) > 0:

                    def get_greater(frames, current_frame):
                        min = sorted((i for i in frames if i < current_frame))
                        return min[-1] if len(min) > 0 else None

                    def get_lower(frames, current_frame):
                        min = sorted((i for i in frames if i > current_frame))
                        return min[0] if len(min) > 0 else None

                    greater = get_greater(keyframes.keys(), frame)
                    lower = get_lower(keyframes.keys(), frame)

                    if greater is not None and lower is not None:
                        ppos, prot, pscale = keyframes[lower]
                        npos, nrot, nscale = keyframes[greater]
                        pos = calculate_new_vector_linear(
                            (lower, ppos), (greater, npos), frame
                        )
                        rot = calculate_new_vector_linear(
                            (lower, prot), (greater, nrot), frame
                        )
                        scale = calculate_new_vector_linear(
                            (lower, pscale), (greater, nscale), frame
                        )
                        obj._pos = pos
                        obj._rot = rot
                        obj._scale = scale
                    elif greater is not None:
                        pos, rot, scale = keyframes[greater]
                        obj._pos = pos
                        obj._rot = rot
                        obj._scale = scale
                    elif lower is not None:
                        pos, rot, scale = keyframes[lower]
                        obj._pos = pos
                        obj._rot = rot
                        obj._scale = scale
