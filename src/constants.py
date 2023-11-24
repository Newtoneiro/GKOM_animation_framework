"""
Constants defined for other files.
"""


class PYGAME_CONSTANTS:
    """
    Constants for pygame config.
    """

    WIDTH: int = 1600
    HEIGHT: int = 900
    FPS: int = 60


class OPENGL_CONSTANTS:
    """
    Constants for opengl config.
    """

    GL_CONTEXT_MAJOR_VERSION: int = 3
    GL_CONTEXT_MINOR_VERSION: int = 3

    DEFAULT_SCENE_COLOUR: tuple[float] = (0.08, 0.16, 0.18)

    DEFAULT_SHADER: str = "default"


class CAMERA_CONSTANTS:
    """
    Constants for camera config.
    """

    DEFAULT_CAMERA_FOV: float = 50.0
    DEFAULT_CAMERA_NEAR_TRESHOLD: float = 0.1
    DEFAULT_CAMERA_FAR_TRESHOLD: float = 100.0
