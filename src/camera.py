"""
This file contains the Camera class.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.graphics_engine import GraphicsEngine

import glm
from PyQt5.QtCore import Qt

from src.constants import CAMERA_CONSTANTS


class Camera:
    """
    Class for a camera abstraction.
    """

    def __init__(self, app: GraphicsEngine) -> None:
        self._app = app
        self._aspect_ratio = app.win_size[0] / app.win_size[1]

        self._position = CAMERA_CONSTANTS.DEFAULT_CAMERA_POSITION
        self._forward = CAMERA_CONSTANTS.DEFAULT_CAMERA_FORWARD
        self._up = CAMERA_CONSTANTS.DEFAULT_CAMERA_UP
        self._right = CAMERA_CONSTANTS.DEFAULT_CAMERA_RIGHT
        self._yaw = CAMERA_CONSTANTS.DEFAULT_CAMERA_YAW
        self._pitch = CAMERA_CONSTANTS.DEFAULT_CAMERA_PITCH

    # ====== PROPERTIES ====== #

    @property
    def m_proj(self) -> glm.mat4:
        """
        [READ-ONLY] glm.mat4: The projection matrix for the camera.
        """
        return self._get_projection_matrix()

    @property
    def m_view(self) -> glm.mat4:
        """
        [READ-ONLY] glm.mat4: The view matrix for the camera.
        """
        return self._get_view_matrix()

    # ====== PRIVATE METHODS ====== #

    def _get_projection_matrix(self) -> glm.mat4:
        """
        Returns the projection matrix for the camera.

        Returns:
            glm.mat4: The projection matrix for the camera.
        """
        return glm.perspective(
            glm.radians(CAMERA_CONSTANTS.DEFAULT_CAMERA_FOV),
            self._aspect_ratio,
            CAMERA_CONSTANTS.DEFAULT_CAMERA_NEAR_TRESHOLD,
            CAMERA_CONSTANTS.DEFAULT_CAMERA_FAR_TRESHOLD,
        )

    def _get_view_matrix(self) -> glm.mat4:
        """
        Returns the view matrix for the camera.

        Returns:
            glm.mat4: The view matrix for the camera.
        """
        return glm.lookAt(
            self._position, self._position + self._forward, self._up
        )

    def _move(self):
        velocity = CAMERA_CONSTANTS.DEFAULT_CAMERA_SPEED * 3
        direction = self._app._key_pressed
        if direction == Qt.Key_W:
            self._position[0] += velocity * self._forward[0]
            self._position[1] += velocity * self._forward[1]
            self._position[2] += velocity * self._forward[2]
        elif direction == Qt.Key_S:
            self._position[0] -= velocity * self._forward[0]
            self._position[1] -= velocity * self._forward[1]
            self._position[2] -= velocity * self._forward[2]
        elif direction == Qt.Key_A:
            self._position[0] -= velocity * self._right[0]
            self._position[1] -= velocity * self._right[1]
            self._position[2] -= velocity * self._right[2]
        elif direction == Qt.Key_D:
            self._position[0] += velocity * self._right[0]
            self._position[1] += velocity * self._right[1]
            self._position[2] += velocity * self._right[2]
        elif direction == Qt.Key_Space:
            self._position[0] += velocity * self._up[0]
            self._position[1] += velocity * self._up[1]
            self._position[2] += velocity * self._up[2]
        elif direction == Qt.Key_Shift:
            self._position[0] -= velocity * self._up[0]
            self._position[1] -= velocity * self._up[1]
            self._position[2] -= velocity * self._up[2]

    def _rotate(self):
        x, y = self._app._mouse_move
        self._yaw += x * CAMERA_CONSTANTS.DEFAULT_CAMERA_SENSITIVITY / 50
        self._pitch -= y * CAMERA_CONSTANTS.DEFAULT_CAMERA_SENSITIVITY / 50
        self._pitch = max(-89.0, min(89.0, self._pitch))

    def _update_camera_vectors(self) -> None:
        """
        Updates the camera vectors taking rotation into account.
        """
        yaw, pitch = glm.radians(self._yaw), glm.radians(self._pitch)

        self._forward.x = glm.cos(yaw) * glm.cos(pitch)
        self._forward.y = glm.sin(pitch)
        self._forward.z = glm.sin(yaw) * glm.cos(pitch)

        self._forward = glm.normalize(self._forward)
        self._right = glm.normalize(
            glm.cross(self._forward, glm.vec3(0, 1, 0))
        )
        self._up = glm.normalize(glm.cross(self._right, self._forward))

    # ====== PUBLIC METHODS ====== #

    def update(self) -> None:
        """
        Updates the camera.
        """
        self._move()
        self._rotate()
        self._update_camera_vectors()
