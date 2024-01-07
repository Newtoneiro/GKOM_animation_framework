"""
This file contains the main class for the graphics engine.
"""
import logging
import sys

import moderngl as mgl
import pygame as pg

from src.camera import Camera
from src.constants import OPENGL_CONSTANTS, PYGAME_CONSTANTS
from src.light import Light
from src.objects.cube import Cube
from src.objects.model_3d import Model3D

from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import Qt, QTimer
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

class GraphicsEngine(QOpenGLWidget):
    """
    Abstract class for the graphics engine.
    """

    def __init__(
        self, win_size: tuple[int] = (PYGAME_CONSTANTS.WIDTH, PYGAME_CONSTANTS.HEIGHT), parent=None
    ) -> None:
        self._win_size = win_size

        self._time = 0
        self._delta_time = 0

        # Initialize prequisites
        # if not (self._init_context()):
        #     raise RuntimeError("Could not initialize.")

        #self._init_camera()
        #self._init_scene()
        #self._init_light()
        self._parent = parent

        super(GraphicsEngine, self).__init__(parent)
    # ====== INITIALIZATION ====== #

    # def _init_pygame(self) -> bool:
    #     """
    #     Initializes pygame.

    #     Returns:
    #         bool: True if pygame was initialized successfully, False otherwise.
    #     """
    #     try:
    #         pg.init()
    #         # Set the OpenGL versions
    #         pg.display.gl_set_attribute(
    #             pg.GL_CONTEXT_MAJOR_VERSION, OPENGL_CONSTANTS.GL_CONTEXT_MAJOR_VERSION
    #         )
    #         pg.display.gl_set_attribute(
    #             pg.GL_CONTEXT_MINOR_VERSION, OPENGL_CONSTANTS.GL_CONTEXT_MINOR_VERSION
    #         )
    #         pg.display.gl_set_attribute(
    #             pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE
    #         )
    #         # Create the context
    #         pg.display.set_mode(self._win_size, flags=pg.DOUBLEBUF | pg.OPENGL)
    #         # Capture mouse
    #         pg.event.set_grab(True)
    #         pg.mouse.set_visible(False)
    #         # Create clock object for time management
    #         self._clock = pg.time.Clock()

        # except pg.error as err:
        #     logging.error(f"Could not initialize pygame: {err}")
        #     return False

        # return True

    def _init_context(self) -> bool:
        """
        Initializes the moderngl context.

        Returns:
            bool: True if the moderngl context was initialized successfully,
            False otherwise.
        """
        try:
            self._mgl_context = mgl.create_context()
            self._mgl_context.enable(mgl.DEPTH_TEST | mgl.CULL_FACE)
        except mgl.Error as err:
            logging.error(f"Could not initialize moderngl: {err}")
            return False

        return True

    def _init_camera(self) -> None:
        """
        Initializes the camera.
        """
        self._camera = Camera(self)

    def _init_scene(self) -> None:
        """
        Initializes the scene.
        """
        self._scene = [
            Cube(
                self,
                texture_path="src/textures/crate.png",
                pos=(-2.5, 0, 0),
                rot=(45, 0, 0),
                scale=(1, 2, 1),
            ),
            Cube(
                self,
                texture_path="src/textures/crate.png",
                pos=(2.5, 0, 0),
                rot=(0, 0, 45),
                scale=(1, 1, 2),
            ),
            Model3D(
                self,
                texture_path="src/models/cat/20430_cat_diff_v1.jpg",
                object_path="src/models/cat/20430_Cat_v1_NEW.obj",
                scale=(0.2, 0.2, 0.2),
            ),
        ]

    def _init_light(self) -> None:
        """
        Initializes the light.
        """
        self._light = Light()

    # ====== PROPERTIES ====== #

    @property
    def time(self) -> float:
        """
        [READ-ONLY] Returns the time since the last frame.

        Returns:
            float: The time since the last frame.
        """
        return self._time

    @property
    def delta_time(self) -> float:
        """
        [READ-ONLY] Returns the delta time.

        Returns:
            float: The delta time.
        """
        return self._delta_time

    @property
    def win_size(self) -> tuple[int]:
        """
        [READ-ONLY] Returns the window size.

        Returns:
            tuple[int]: The window size.
        """
        return self._win_size

    @property
    def mgl_context(self) -> mgl.Context:
        """
        [READ-ONLY] Returns the moderngl context.

        Returns:
            mgl.Context: The moderngl context.
        """
        return self._mgl_context

    @property
    def camera(self) -> Camera:
        """
        [READ-ONLY] Returns the camera.

        Returns:
            Camera: The camera.
        """
        return self._camera

    @property
    def light(self) -> Light:
        """
        [READ-ONLY] Returns the light.

        Returns:
            Light: The light.
        """
        return self._light

    def _check_events(self) -> None:
        """
        Handles pygame events.
        """
        # Key down events
        for event in pg.event.get():
            self._event_callbacks.get(event.type, lambda _: None)(event)

    def _render(self) -> None:
        """
        Renders the scene.
        """
        self._mgl_context.clear(color=OPENGL_CONSTANTS.DEFAULT_SCENE_COLOUR)
        for obj in self._scene:
            obj.render()
        pg.display.flip()

    def _update_time(self) -> None:
        """
        Updates the time.
        """
        self._time = pg.time.get_ticks() / 1000
        self._delta_time = self._clock.tick(PYGAME_CONSTANTS.FPS)

    # ====== EVENT CALLBACKS ====== #

    def _init_event_callbacks(self) -> None:
        """
        Initializes event callbacks.
        """
        self._event_callbacks = {
            pg.QUIT: lambda _: self._handle_stop(),
            pg.KEYDOWN: lambda event: self._handle_key_down(event.key),
        }

        self._key_down_callbacks = {
            pg.K_ESCAPE: self._handle_stop,
        }

    def _handle_stop(self) -> None:
        """
        Handles the stop event.
        """
        for obj in self._scene:
            obj.destroy()
        pg.quit()
        sys.exit()

    def _handle_key_down(self, event_key: int) -> None:
        """
        Handles the key down event.
        """
        if event_key in self._key_down_callbacks:
            self._key_down_callbacks[event_key]()

    # ====== PUBLIC METHODS ====== #
    def initializeGL(self) -> None:
        if not (self._init_context()):
            raise RuntimeError("Could not initialize.")
        self._init_camera()
        #loading textures needs rewriting
        #self._init_scene()
        self._init_light()

    def resizeGL(self, w, h) -> None:
        self._mgl_context.viewport = (0, 0, self.width(), self.height())

    def paintGL(self) -> None:
        self._mgl_context.clear(color=(0.08, 0.16, 0.18, 1))
        #camera and light movement needs rewriting
        #self._camera.update()
        #self._light.update()
        #self._render()
        self._mgl_context.finish()
    
    # def run(self) -> None:
    #     """
    #     Runs the graphics engine.
    #     """
    #     self._init_event_callbacks()
    #     while True:
    #         self._check_events()
    #         self._camera.update()
    #         self._light.update()
    #         self._render()
    #         self._update_time()

