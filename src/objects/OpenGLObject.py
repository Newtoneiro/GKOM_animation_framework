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
import glm

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

    # ====== STATIC METHODS ====== #

    @staticmethod
    def get_data(vertices: np.array, indices: np.array) -> np.ndarray:
        """
        Returns the vertex data for the OpenGlObject.

        Args:
            vertices (np.array): The vertices of the OpenGlObject.
            indices (np.array): The indices of the OpenGlObject.

        Returns:
            np.ndarray: The vertex data for the OpenGlObject.
        """
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype=np.float32)

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

    def _get_model_matrix(self) -> np.ndarray:
        """
        Returns the model matrix for the OpenGlObject.

        Returns:
            np.ndarray: The model matrix for the OpenGlObject.
        """
        return glm.mat4()

    def _write_camera(self) -> None:
        """
        Writes the camera to the shader program.
        """
        self._shader_program["m_proj"].write(self._app.camera.m_proj)
        self._shader_program["m_view"].write(self._app.camera.m_view)
        self._shader_program["m_model"].write(self.m_model)

    # ====== PROPERTIES ====== #

    @property
    def m_model(self) -> glm.mat4:
        """
        [READ-ONLY] glm.mat4: The model matrix for the OpenGlObject.
        """
        return self._get_model_matrix()

    # ====== PUBLIC METHODS ====== #

    def update(self) -> None:  # TMP to show the spin
        """
        Spins the OpenGlObject.
        """
        m_model = glm.rotate(self.m_model, self._app.time, glm.vec3(0, 1, 0))
        self._shader_program["m_model"].write(m_model)

    def render(self) -> None:
        """
        Renders the OpenGlObject.
        """
        if not self._pre_rendered:
            self._pre_render()

        self._write_camera()
        self.update()  # tmp to show the spin
        self._vao.render()

    def destroy(self) -> None:
        """
        Destroys the OpenGlObject.
        """
        self._vbo.release()
        self._shader_program.release()
        self._vao.release()