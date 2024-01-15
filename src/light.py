"""
This file contains the Light class.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.graphics_engine import GraphicsEngine

import glm
from PyQt5.QtCore import Qt

from src.constants import LIGHT_CONSTANTS


class Light:
    """
    Class for a light abstraction.
    """

    def __init__(self, app: GraphicsEngine) -> None:
        self._app = app
        self._position = LIGHT_CONSTANTS.DEFAULT_LIGHT_POSITION
        self._color = LIGHT_CONSTANTS.DEFAULT_LIGHT_COLOR
        self._ambient = LIGHT_CONSTANTS.DEFAULT_LIGHT_AMBIENT * self._color
        self._diffuse = LIGHT_CONSTANTS.DEFAULT_LIGHT_DIFFUSE * self._color
        self._specular = LIGHT_CONSTANTS.DEFAULT_LIGHT_SPECULAR * self._color

    @property
    def position(self) -> glm.vec3:
        """
        [READ-ONLY] Returns the position of the light.

        Returns:
            glm.vec3: The position of the light.
        """
        return self._position

    @property
    def color(self) -> glm.vec3:
        """
        [READ-ONLY] Returns the color of the light.

        Returns:
            glm.vec3: The color of the light.
        """
        return self._color

    @property
    def ambient(self) -> float:
        """
        [READ-ONLY] Returns the ambient of the light.

        Returns:
            float: The ambient of the light.
        """
        return self._ambient

    @property
    def diffuse(self) -> float:
        """
        [READ-ONLY] Returns the diffuse of the light.

        Returns:
            float: The diffuse of the light.
        """
        return self._diffuse

    @property
    def specular(self) -> float:
        """
        [READ-ONLY] Returns the specular of the light.

        Returns:
            float: The specular of the light.
        """
        return self._specular

    def _move(self) -> None:
        """
        Moves the light.
        """
        step = LIGHT_CONSTANTS.DEFAULT_LIGHT_STEP
        key = self._app._key_pressed
        if key == Qt.Key_Up:
            self._position[1] += step
        elif key == Qt.Key_Down:
            self._position[1] -= step
        elif key == Qt.Key_Right:
            self._position[0] += step
        elif key == Qt.Key_Left:
            self._position[0] -= step
        elif key == Qt.Key_4:
            self._position[2] += step
        elif key == Qt.Key_6:
            self._position[2] -= step

    def update(self) -> None:
        """
        Updates the light.
        """
        self._move()
