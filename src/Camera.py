"""
This file contains the Camera class.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.graphicsEngine import GraphicsEngine

import pygame as pg
import glm

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
            self._position + self._forward,
            self._up
        )

    def _move(self) -> None:
        """
        Moves the camera.
        """
        velocity = CAMERA_CONSTANTS.DEFAULT_CAMERA_SPEED * self._app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self._position += velocity * self._forward
        if keys[pg.K_s]:
            self._position -= velocity * self._forward
        if keys[pg.K_a]:
            self._position -= velocity * self._right
        if keys[pg.K_d]:
            self._position += velocity * self._right
        if keys[pg.K_SPACE]:
            self._position += velocity * self._up
        if keys[pg.K_LSHIFT]:
            self._position -= velocity * self._up

    def _rotate(self) -> None:
        """
        Rotates the camera.
        """
        rel_x, rel_y = pg.mouse.get_rel()
        self._yaw += rel_x * CAMERA_CONSTANTS.DEFAULT_CAMERA_SENSITIVITY
        self._pitch -= rel_y * CAMERA_CONSTANTS.DEFAULT_CAMERA_SENSITIVITY
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
