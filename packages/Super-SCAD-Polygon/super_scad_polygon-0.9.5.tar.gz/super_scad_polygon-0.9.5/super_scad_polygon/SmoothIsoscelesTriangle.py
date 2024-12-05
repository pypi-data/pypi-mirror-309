from typing import List, Set

from super_scad_smooth_profile.SmoothProfile import SmoothProfile

from super_scad_polygon.IsoscelesTriangle import IsoscelesTriangle
from super_scad_polygon.SmoothPolygonMixin import SmoothPolygonMixin


class SmoothIsoscelesTriangle(SmoothPolygonMixin, IsoscelesTriangle):
    """
    A widget for isosceles triangles with smooth corners.
    """

    # ----------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 width: float,
                 isosceles_length: float | None = None,
                 depth: float | None = None,
                 center: bool = False,
                 profiles: SmoothProfile | List[SmoothProfile] | None = None,
                 extend_sides_by_eps: bool | List[bool] | Set[int] | None = None):
        """
        Object constructor.

        :param width: The length of the base of the isosceles triangle.
        :param isosceles_length: The length of the isosceles sides of the isosceles triangle.
        :param depth: The depth of the isosceles triangle.
        :param center: Whether the triangle must be centered with its point of mass at the origin.
        :param profiles: The profile to be applied at nodes of the right triangle. When a single profile is given, this
                         profile will be applied at all nodes.
        :param extend_sides_by_eps: Whether to extend sides by eps for a clear overlap.
        """
        IsoscelesTriangle.__init__(self,
                                   width=width,
                                   isosceles_length=isosceles_length,
                                   depth=depth,
                                   center=center,
                                   extend_sides_by_eps=extend_sides_by_eps)
        SmoothPolygonMixin.__init__(self, profiles=profiles)

# ----------------------------------------------------------------------------------------------------------------------
