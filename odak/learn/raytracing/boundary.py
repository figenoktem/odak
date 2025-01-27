import torch
from odak.learn.raytracing.primitives import is_it_on_triangle, center_of_triangle


def intersect_w_triangle(ray, triangle):
    """
    Definition to find intersection point of a ray with a triangle. Returns False for each variable if the ray doesn't intersect with a given triangle.

    Parameters
    ----------
    ray          : torch.tensor
                   A vector/ray.
    triangle     : torch.tensor
                   Set of points in X,Y and Z to define a single triangle.

    Returns
    ----------
    normal       : torch.tensor
                   Surface normal at the point of intersection.
    distance     : float
                   Distance in between a starting point of a ray and the intersection point with a given triangle.
    """
    normal, distance = intersect_w_surface(ray, triangle)
    if is_it_on_triangle(normal[0], triangle[0], triangle[1], triangle[2]) == False:
        return 0, 0
    return normal, distance


def intersect_w_surface(ray, points):
    """
    Definition to find intersection point inbetween a surface and a ray. For more see: http://geomalgorithms.com/a06-_intersect-2.html

    Parameters
    ----------
    ray          : torch.tensor
                   A vector/ray.
    points       : torch.tensor
                   Set of points in X,Y and Z to define a planar surface.

    Returns
    ----------
    normal       : torch.tensor
                   Surface normal at the point of intersection.
    distance     : float
                   Distance in between starting point of a ray with it's intersection with a planar surface.
    """
    points = torch.tensor(points)
    normal = get_triangle_normal(points)
    if len(ray.shape) == 2:
        ray = ray.reshape((1, 2, 3))
    if len(points) == 2:
        points = points.reshape((1, 3, 3))
    if len(normal.shape) == 2:
        normal = normal.reshape((1, 2, 3))
    f = normal[:, 0]-ray[:, 0]
    distance = torch.mm(normal[:, 1], f.T)/torch.mm(normal[:, 1], ray[:, 1].T)
    n = int((torch.max(torch.tensor([ray.shape[0], normal.shape[0]]))))
    normal = torch.zeros((n, 2, 3))
    normal[:, 0] = ray[:, 0] + distance.T*ray[:, 1]
    distance = torch.abs(distance)
    if normal.shape[0] == 1:
        normal = normal.reshape((2, 3))
        distance = distance.reshape((1))
    if distance.shape[0] == 1 and len(distance.shape) > 1:
        distance = distance.reshape((distance.shape[1]))
    return normal, distance


def get_triangle_normal(triangle, triangle_center=None):
    """
    Definition to calculate surface normal of a triangle.

    Parameters
    ----------
    triangle        : torch.tensor
                      Set of points in X,Y and Z to define a planar surface (3,3). It can also be list of triangles (mx3x3).
    triangle_center : torch.tensor
                      Center point of the given triangle. See odak.learn.raytracing.center_of_triangle for more. In many scenarios you can accelerate things by precomputing triangle centers.

    Returns
    ----------
    normal          : torch.tensor
                      Surface normal at the point of intersection.
    """
    triangle = torch.tensor(triangle)
    if len(triangle.shape) == 2:
        triangle = triangle.reshape((1, 3, 3))
    normal = torch.zeros((triangle.shape[0], 2, 3)).to(triangle.device)
    direction = torch.cross(
        triangle[:, 0]-triangle[:, 1], triangle[:, 2]-triangle[:, 1])
    if type(triangle_center) == type(None):
        normal[:, 0] = center_of_triangle(triangle)
    else:
        normal[:, 0] = triangle_center
    normal[:, 1] = direction/torch.sum(direction, axis=1)[0]
    if normal.shape[0] == 1:
        normal = normal.reshape((2, 3))
    return normal


