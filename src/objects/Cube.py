"""
This file contains the Cube class.
"""
import numpy as np

from src.objects.OpenGLObject import OpenGLObject


class Cube(OpenGLObject):
    """
    Class for a cube abstraction.
    """

    def _get_vertex_data(self) -> np.ndarray:
        """
        Returns the vertex data for the cube.

        Returns:
            np.ndarray: The vertex data for the cube.
        """
        vertices = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
                    (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]
        indices = [(0, 2, 3), (0, 1, 2), (1, 5, 2), (5, 6, 2),
                   (6, 7, 2), (7, 3, 2), (7, 4, 3), (4, 0, 3),
                   (4, 5, 0), (5, 1, 0), (7, 6, 4), (6, 5, 4)]
        return self.get_data(vertices, indices)
