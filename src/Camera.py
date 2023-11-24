"""
This file contains the Camera class.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.GraphicsEngine import GraphicsEngine

import glm

from src.constants import CAMERA_CONSTANTS


class Camera:
    """
    Class for a camera abstraction.
    """
    def __init__(self, app: GraphicsEngine) -> None:
        self._app = app
        self._aspect_ratio = app.win_size[0] / app.win_size[1]
        self._position = glm.vec3(2, 3, 3)

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
            CAMERA_CONSTANTS.DEFAULT_CAMERA_FAR_TRESHOLD
        )

    def _get_view_matrix(self) -> glm.mat4:
        """
        Returns the view matrix for the camera.

        Returns:
            glm.mat4: The view matrix for the camera.
        """
        return glm.lookAt(
            self._position,
            self._position + glm.vec3(0, 0, -1),
            glm.vec3(0, 1, 0)
        )

    # ====== PUBLIC METHODS ====== #

    def move(self, update_vector: glm.vec3) -> None:
        """
        Moves the camera.
        """
        self._position += update_vector
