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
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                pg.quit()
                sys.exit()

    def _render(self) -> None:
        """
        Renders the scene.
        """
        self._mgl_context.clear(*OPENGL_CONSTANTS.DEFAULT_SCENE_COLOUR)
        pg.display.flip()

    def run(self) -> None:
        """
        Runs the graphics engine.
        """
        while True:
            self._check_events()
            self._render()
            self._clock.tick(PYGAME_CONSTANTS.FPS)
