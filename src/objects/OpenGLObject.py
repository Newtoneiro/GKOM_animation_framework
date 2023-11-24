"""
This file contains the abstract Object class.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.GraphicsEngine import GraphicsEngine

from abc import ABC, abstractmethod
import numpy as np
import moderngl as mgl

from src.constants import OPENGL_CONSTANTS


class OpenGLObject(ABC):
    """
    Class for an OpenGlObject.
    """

    def __init__(
        self,
        app: GraphicsEngine,
        shader_program: str = OPENGL_CONSTANTS.DEFAULT_SHADER,
        pre_render: bool = True,
    ) -> None:
        self._app = app
        self._shader_program = shader_program
        self._mgl_context = app.mgl_context
        self._shader_program = shader_program

        if pre_render:
            self._pre_render()

    # ====== ABSTRACT METHODS ====== #

    @abstractmethod
    def _get_vertex_data(self) -> np.ndarray:
        ...

    # ====== PRIVATE METHODS ====== #

    def _pre_render(self) -> None:
        """
        Pre-renders the OpenGlObject.
        """
        self._vbo = self._get_vbo()
        self._shader_program = self._get_shader_program(
            self._shader_program
        )
        self._vao = self._get_vao()

        self._pre_rendered = True

    def _get_vbo(self) -> mgl.Buffer:
        """
        Returns the vertex buffer object for the OpenGlObject.

        Returns:
            mgl.Buffer: The vertex buffer object for the OpenGlObject.
        """
        return self._mgl_context.buffer(self._get_vertex_data())

    def _get_vao(self) -> mgl.VertexArray:
        """
        Returns the vertex array object for the OpenGlObject.

        Returns:
            mgl.VertexArray: The vertex array object for the OpenGlObject.
        """
        return self._mgl_context.vertex_array(
            self._shader_program, [(self._vbo, "3f", "in_position")]
        )

    def _get_shader_program(self, shader_name: str) -> mgl.Program:
        """
        Returns the shader program for the OpenGlObject.

        Args:
            shader_name (str): The name of the shader program.

        Returns:
            mgl.Program: The shader program for the OpenGlObject.
        """
        with open(f"src/shaders/{shader_name}.vert", "r") as f:
            vertex_shader_source = f.read()

        with open(f"src/shaders/{shader_name}.frag", "r") as f:
            fragment_shader_source = f.read()

        program = self._mgl_context.program(
            vertex_shader=vertex_shader_source,
            fragment_shader=fragment_shader_source
        )

        return program

    # ====== PUBLIC METHODS ====== #

    def render(self) -> None:
        """
        Renders the OpenGlObject.
        """
        if not self._pre_rendered:
            self._pre_render()

        self._vao.render()

    def destroy(self) -> None:
        """
        Destroys the OpenGlObject.
        """
        self._vbo.release()
        self._shader_program.release()
        self._vao.release()
