"""
This file contains the main class for the graphics engine.
"""
import pygame as pg
import moderngl as mgl
import sys
import logging

from src.constants import PYGAME_CONSTANTS, OPENGL_CONSTANTS


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

        if not self._init_pygame():
            raise RuntimeError("Could not initialize pygame.")

    def _init_pygame(self) -> bool:
        """
        Initializes pygame.
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
            # Detect and use existing OpenGL context
            self._mgl_context = mgl.create_context()
            # Create clock object for time management
            self._clock = pg.time.Clock()
        except pg.error as err:
            logging.error(f"Could not initialize pygame: {err}")
            return False

        return True

    def _check_events(self) -> None:
        """
        Handles pygame events.
        """
        for event in pg.event.get():
            self._event_callbacks.get(event.type, lambda _: None)(event)

    def _render(self) -> None:
        """
        Renders the scene.
        """
        self._mgl_context.clear(color=OPENGL_CONSTANTS.DEFAULT_SCENE_COLOUR)
        pg.display.flip()

    # ====== EVENT CALLBACKS ====== #

    def _init_event_callbacks(self) -> None:
        """
        Initializes event callbacks.
        """
        self._event_callbacks = {
            pg.QUIT: lambda _: self._handle_stop(),
            pg.KEYDOWN: lambda event: self._handle_key_down(event.key),
        }

        self._key_callbacks = {
            pg.K_ESCAPE: self._handle_stop,
        }

    def _handle_stop(self) -> None:
        """
        Handles the stop event.
        """
        pg.quit()
        sys.exit()

    def _handle_key_down(self, event_key: int) -> None:
        """
        Handles the key down event.
        """
        if event_key in self._key_callbacks:
            self._key_callbacks[event_key]()

    def run(self) -> None:
        """
        Runs the graphics engine.
        """
        self._init_event_callbacks()
        while True:
            self._check_events()
            self._render()
            self._clock.tick(PYGAME_CONSTANTS.FPS)
