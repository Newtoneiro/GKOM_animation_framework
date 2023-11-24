"""
This file contains the Triangle class.
"""
import numpy as np

from src.objects.OpenGLObject import OpenGLObject


class Triangle(OpenGLObject):
    """
    Class for a triangle.
    """

    def _get_vertex_data(self) -> np.ndarray:
        """
        Returns the vertex data for the triangle.

        Returns:
            np.ndarray: The vertex data for the triangle.
        """
        vertex_data = [(-0.6, -0.8, 0.0), (0.6, -0.8, 0.0), (0.0, 0.8, 0.0)]
        vertex_data = np.array(vertex_data, dtype=np.float32)
        return vertex_data
