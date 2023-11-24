"""
This file contains the Cube class.
"""
import numpy as np

from src.objects.openGLObject import OpenGLObject


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
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]
        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]

        vertex_data = self.get_data(vertices, indices)

        if self._texture is not None:
            tex_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]
            tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                                 (0, 2, 3), (0, 1, 2),
                                 (0, 1, 2), (2, 3, 0),
                                 (2, 3, 0), (2, 0, 1),
                                 (0, 2, 3), (0, 1, 2),
                                 (3, 1, 2), (3, 0, 1)]
            tex_coord_data = self.get_data(tex_coords, tex_coord_indices)
            vertex_data = np.hstack([tex_coord_data, vertex_data])

        return vertex_data
