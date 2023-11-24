"""
This file contains the Triangle class.
"""
import numpy as np
import moderngl as mgl

from src.classes import GraphicsEngine
from src.constants import OPENGL_CONSTANTS


class Triangle:
    """
    Class for a triangle.
    """
    def __init__(self, app: GraphicsEngine, pre_render: bool = True) -> None:
        self._app = app
        self.mgl_context = app.mgl_context

        if pre_render:
            self._pre_render()

    def _pre_render(self) -> None:
        """
        Pre-renders the triangle.
        """
        self._vbo = self._get_vbo()
        self._shader_program = self._get_shader_program(
            OPENGL_CONSTANTS.DEFAULT_SHADER
            )
        self._vao = self._get_vao()

        self._pre_rendered = True

    def _get_vertex_data(self) -> np.ndarray:
        """
        Returns the vertex data for the triangle.

        Returns:
            np.ndarray: The vertex data for the triangle.
        """
        vertex_data = [(-0.6, -0.8, 0.0), (0.6, -0.8, 0.0), (0.0, 0.8, 0.0)]
        vertex_data = np.array(vertex_data, dtype=np.float32)
        return vertex_data

    def _get_vbo(self) -> mgl.Buffer:
        """
        Returns the vertex buffer object for the triangle.

        Returns:
            mgl.Buffer: The vertex buffer object for the triangle.
        """
        return self.mgl_context.buffer(self._get_vertex_data())

    def _get_vao(self) -> mgl.VertexArray:
        """
        Returns the vertex array object for the triangle.

        Returns:
            mgl.VertexArray: The vertex array object for the triangle.
        """
        return self.mgl_context.vertex_array(
            self._shader_program, [(self._vbo, "3f", "in_position")]
            )

    def _get_shader_program(self, shader_name: str) -> mgl.Program:
        """
        Returns the shader program for the triangle.

        Args:
            shader_name (str): The name of the shader program.

        Returns:
            mgl.Program: The shader program for the triangle.
        """
        with open(f"src/shaders/{shader_name}.vert", "r") as f:
            vertex_shader_source = f.read()

        with open(f"src/shaders/{shader_name}.frag", "r") as f:
            fragment_shader_source = f.read()

        program = self.mgl_context.program(
            vertex_shader=vertex_shader_source,
            fragment_shader=fragment_shader_source
        )

        return program

    def render(self) -> None:
        """
        Renders the triangle.
        """
        if not self._pre_rendered:
            self._pre_render()

        self._vao.render()

    def destroy(self) -> None:
        """
        Destroys the triangle.
        """
        self._vbo.release()
        self._shader_program.release()
        self._vao.release()
