"""
Constants defined for other files.
"""


import glm


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
    DEFAULT_CAMERA_SPEED: float = 0.01
    DEFAULT_CAMERA_SENSITIVITY: float = 0.05

    DEFAULT_CAMERA_POSITION: glm.vec3 = glm.vec3(0, 0, 4)
    DEFAULT_CAMERA_FORWARD: glm.vec3 = glm.vec3(0, 0, -1)
    DEFAULT_CAMERA_UP: glm.vec3 = glm.vec3(0, 1, 0)
    DEFAULT_CAMERA_RIGHT: glm.vec3 = glm.vec3(1, 0, 0)
    DEFAULT_CAMERA_YAW: float = -90.0
    DEFAULT_CAMERA_PITCH: float = 0.0
