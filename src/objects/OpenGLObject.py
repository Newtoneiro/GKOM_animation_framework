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
import pygame as pg
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
        texture_path: str = None,
        pos: tuple[float] = (0, 0, 0),
        rot: tuple[float] = (0, 0, 0),
        scale: tuple[float] = (1, 1, 1)
    ) -> None:
        self._app = app
        self._pos = pos
        self._rot = glm.vec3([glm.radians(a) for a in rot])
        self._scale = scale
        self._shader_program = shader_program
        self._mgl_context = app.mgl_context
        self._shader_program = shader_program
        self.texture = texture_path

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
        if self._texture is not None:
            vertex_array = self._mgl_context.vertex_array(
                self._shader_program, [
                    (self._vbo, "2f 3f 3f", "in_texcoord_0", "in_normal", "in_position")
                    ]
                )
        else:
            vertex_array = self._mgl_context.vertex_array(
                self._shader_program, [(self._vbo, "3f", "in_position")]
                )

        return vertex_array

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
        m_model = glm.mat4()
        m_model = self._get_translation_matrix(m_model)
        m_model = self._get_rotation_matrix(m_model)
        m_model = self._get_scaling_matrix(m_model)
        return m_model
    
    def _get_translation_matrix(self, m_model) -> np.ndarray:
        """
        Returns the model translation matrix for the OpenGlObject.

        Args:
            m_model (np.ndarray): The model matrix.

        Returns:
            np.ndarray: The model translation matrix for the OpenGlObject.
        """
        return glm.translate(m_model, self._pos)
    
    def _get_rotation_matrix(self, m_model) -> np.ndarray:
        """
        Returns the model rotation matrix for the OpenGlObject.

        Args:
            m_model (np.ndarray): The model matrix.

        Returns:
            np.ndarray: The model rotation matrix for the OpenGlObject.
        """
        m_model = glm.rotate(m_model, self._rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self._rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self._rot.z, glm.vec3(0, 0, 1))
        return m_model
    
    def _get_scaling_matrix(self, m_model) -> np.ndarray:
        """
        Returns the model scaling matrix for the OpenGlObject.

        Args:
            m_model (np.ndarray): The model matrix.

        Returns:
            np.ndarray: The model scaling matrix for the OpenGlObject.
        """
        return glm.scale(m_model, self._scale)


    def _write_shader(self) -> None:
        """
        Writes the pvm to the shader program.
        """
        self._write_texture()
        self._write_lighing()

        self._shader_program["m_proj"].write(self._app.camera.m_proj)
        self._shader_program["m_view"].write(self._app.camera.m_view)
        self._shader_program["m_model"].write(self.m_model)

    def _write_texture(self) -> None:
        """
        Writes the texture to the shader program.
        """
        if self.texture is not None:
            self._shader_program["u_texture_0"] = 0
            self._texture.use()

    def _write_lighing(self) -> None:
        """
        Writes the lighting to the shader program.
        """
        self._shader_program["light.position"].write(self._app._light.position)
        self._shader_program["light.Ia"].write(self._app._light.Ia)
        self._shader_program["light.Id"].write(self._app._light.Id)
        self._shader_program["light.Is"].write(self._app._light.Is)

    def _load_texture(self, texture_path: str) -> mgl.Texture:
        """
        Returns the texture for the OpenGlObject.

        Returns:
            mgl.Texture: The texture for the OpenGlObject.

        Args:
            texture_path (str): The path to the texture.
        """
        texture = pg.image.load(texture_path).convert()
        # Flip because Pygame's y-axis is inverted
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self._mgl_context.texture(
            size=texture.get_size(),
            components=3,
            data=pg.image.tostring(texture, "RGB")
        )
        return texture

    # ====== PROPERTIES ====== #

    @property
    def m_model(self) -> glm.mat4:
        """
        [READ-ONLY] glm.mat4: The model matrix for the OpenGlObject.
        """
        return self._get_model_matrix()

    @property
    def texture(self) -> mgl.Texture:
        """
        mgl.Texture: The texture for the OpenGlObject.
        """
        return self._texture

    @texture.setter
    def texture(self, texture_path: str) -> None:
        """
        Sets the texture for the OpenGlObject.

        Args:
            texture_path (str): The path to the texture.
        """
        if texture_path is not None:
            self._texture = self._load_texture(texture_path)
        else:
            self._texture = None

    # ====== PUBLIC METHODS ====== #

    def update(self) -> None:  # TMP to show the spin
        """
        Spins the OpenGlObject.
        """
        m_model = glm.rotate(self.m_model, self._app.time, glm.vec3(0, 1, 0))
        self._shader_program["m_model"].write(m_model)
        self._shader_program["m_view"].write(self._app.camera.m_view)
        self._shader_program["camPos"].write(self._app.camera._position)

    def render(self) -> None:
        """
        Renders the OpenGlObject.
        """
        if not self._pre_rendered:
            self._pre_render()

        self._write_shader()
        self.update()  # tmp to show the spin
        self._vao.render()

    def destroy(self) -> None:
        """
        Destroys the OpenGlObject.
        """
        self._vbo.release()
        self._shader_program.release()
        self._vao.release()
