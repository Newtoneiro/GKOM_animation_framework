"""
This file contains the main class for the graphics engine.
"""
import pygame as pg
import moderngl as mgl
import sys
import logging
import glm

from src.constants import PYGAME_CONSTANTS, OPENGL_CONSTANTS, CAMERA_CONSTANTS
from src.objects.cube import Cube
from src.camera import Camera


class GraphicsEngine:
    """
    Abstract class for the graphics engine.
    """

    def __init__(
        self, win_size: tuple[int] = (
            PYGAME_CONSTANTS.WIDTH, PYGAME_CONSTANTS.HEIGHT
            )
    ) -> None:
        self._win_size = win_size

        self._time = 0
        self._delta_time = 0

        # Initialize prequisites
        if not all([self._init_pygame(), self._init_context()]):
            raise RuntimeError("Could not initialize.")

        self._init_camera()
        self._init_scene()

    # ====== INITIALIZATION ====== #

    def _init_pygame(self) -> bool:
        """
        Initializes pygame.

        Returns:
            bool: True if pygame was initialized successfully, False otherwise.
        """
        try:
            pg.init()
            # Set the OpenGL versions
            pg.display.gl_set_attribute(
                pg.GL_CONTEXT_MAJOR_VERSION,
                OPENGL_CONSTANTS.GL_CONTEXT_MAJOR_VERSION
            )
            pg.display.gl_set_attribute(
                pg.GL_CONTEXT_MINOR_VERSION,
                OPENGL_CONSTANTS.GL_CONTEXT_MINOR_VERSION
            )
            pg.display.gl_set_attribute(
                pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE
            )
            # Create the context
            pg.display.set_mode(self._win_size, flags=pg.DOUBLEBUF | pg.OPENGL)
            # Create clock object for time management
            self._clock = pg.time.Clock()

        except pg.error as err:
            logging.error(f"Could not initialize pygame: {err}")
            return False

        return True

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
        self._scene = Cube(self, texture_path="src/textures/crate.png")

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

    def _check_events(self) -> None:
        """
        Handles pygame events.
        """
        # Key down events
        for event in pg.event.get():
            self._event_callbacks.get(event.type, lambda _: None)(event)

        # Key pressed events
        if any(pg.key.get_pressed()):
            for key, callback in self._key_pressed_callbacks.items():
                if pg.key.get_pressed()[key]:
                    callback()

    def _render(self) -> None:
        """
        Renders the scene.
        """
        self._mgl_context.clear(color=OPENGL_CONSTANTS.DEFAULT_SCENE_COLOUR)
        if self._scene:
            self._scene.render()
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

        self._key_pressed_callbacks = {
            pg.K_w: self._handle_camera_move_forward,
            pg.K_s: self._handle_camera_move_backward,
            pg.K_a: self._handle_camera_move_left,
            pg.K_d: self._handle_camera_move_right,
            pg.K_q: self._handle_camera_move_up,
            pg.K_e: self._handle_camera_move_down,
        }

    def _handle_stop(self) -> None:
        """
        Handles the stop event.
        """
        if self._scene:
            self._scene.destroy()
        pg.quit()
        sys.exit()

    def _handle_key_down(self, event_key: int) -> None:
        """
        Handles the key down event.
        """
        if event_key in self._key_down_callbacks:
            self._key_down_callbacks[event_key]()

    def _camera_move(self, update_vector: glm.vec3) -> None:
        """
        Handles the camera movement.
        """
        velocity = CAMERA_CONSTANTS.DEFAULT_CAMERA_SPEED * self._delta_time
        self._camera.move(update_vector * velocity)

    def _handle_camera_move_forward(self) -> None:
        """
        Handles the camera movement forward.
        """
        self._camera_move(glm.vec3(0, 0, -1))

    def _handle_camera_move_backward(self) -> None:
        """
        Handles the camera movement backward.
        """
        self._camera_move(glm.vec3(0, 0, 1))

    def _handle_camera_move_left(self) -> None:
        """
        Handles the camera movement left.
        """
        self._camera_move(glm.vec3(-1, 0, 0))

    def _handle_camera_move_right(self) -> None:
        """
        Handles the camera movement right.
        """
        self._camera_move(glm.vec3(1, 0, 0))

    def _handle_camera_move_up(self) -> None:
        """
        Handles the camera movement up.
        """
        self._camera_move(glm.vec3(0, 1, 0))

    def _handle_camera_move_down(self) -> None:
        """
        Handles the camera movement down.
        """
        self._camera_move(glm.vec3(0, -1, 0))

    # ====== PUBLIC METHODS ====== #

    def run(self) -> None:
        """
        Runs the graphics engine.
        """
        self._init_event_callbacks()
        while True:
            self._check_events()
            self._render()
            self._update_time()
