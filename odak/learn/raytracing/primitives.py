import torch
from odak.learn.tools.vector import same_side


def center_of_triangle(triangle):
    """
    Definition to calculate center of a triangle.

    Parameters
    ----------
    triangle      : torch.tensor
                    An array that contains three points defining a triangle (Mx3). It can also parallel process many triangles (NxMx3).
    """
    if len(triangle.shape) == 2:
        triangle = triangle.reshape((1, 3, 3))
    center = torch.mean(triangle, axis=1)
    return center


def is_it_on_triangle(pointtocheck, point0, point1, point2):
    """
    Definition to check if a given point is inside a triangle. If the given point is inside a defined triangle, this definition returns True.

    Parameters
    ----------
    pointtocheck  : list
                    Point to check.
    point0        : list
                    First point of a triangle.
    point1        : list
                    Second point of a triangle.
    point2        : list
                    Third point of a triangle.
    """
    # point0, point1 and point2 are the corners of the triangle.
    pointtocheck = torch.tensor(pointtocheck).reshape(3)
    point0 = torch.tensor(point0)
    point1 = torch.tensor(point1)
    point2 = torch.tensor(point2)
    side0 = same_side(pointtocheck, point0, point1, point2)
    side1 = same_side(pointtocheck, point1, point0, point2)
    side2 = same_side(pointtocheck, point2, point0, point1)
    if side0 == True and side1 == True and side2 == True:
        return True
    return False
