"""
This file contains the Model3D class.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.GraphicsEngine import GraphicsEngine

import numpy as np
import pywavefront

from src.objects.OpenGLObject import OpenGLObject
from src.constants import OPENGL_CONSTANTS


class Model3D(OpenGLObject):
    """
    Class for a Model3D.
    """

    def __init__(
        self,
        app: GraphicsEngine,
        object_path: str,
        shader_program: str = OPENGL_CONSTANTS.DEFAULT_SHADER,
        pre_render: bool = True,
        texture_path: str = None,
        pos: tuple[float] = OPENGL_CONSTANTS.DEFAULT_POSITION,
        rot: tuple[float] = OPENGL_CONSTANTS.DEFAULT_ROTATION,
        scale: tuple[float] = OPENGL_CONSTANTS.DEFAULT_SCALE
    ) -> None:
        self._object_path = object_path
        super().__init__(app, shader_program, pre_render, texture_path, pos, rot, scale)

    def _get_vertex_data(self):
        objs = pywavefront.Wavefront(self._object_path, cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype="f4")
        return vertex_data
