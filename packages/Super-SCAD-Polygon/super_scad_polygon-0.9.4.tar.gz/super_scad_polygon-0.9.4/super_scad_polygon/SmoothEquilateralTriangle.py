from typing import List, Set

from super_scad_smooth_profile.SmoothProfileFactory import SmoothProfileFactory

from super_scad_polygon.EquilateralTriangle import EquilateralTriangle
from super_scad_polygon.SmoothPolygonMixin import SmoothPolygonMixin


class SmoothEquilateralTriangle(SmoothPolygonMixin, EquilateralTriangle):
    """
    A widget for equilateral triangles with smooth corners.
    """

    # ----------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 side_length: float | None = None,
                 depth: float | None = None,
                 center: bool = False,
                 profile_factories: SmoothProfileFactory | List[SmoothProfileFactory] | None = None,
                 extend_sides_by_eps: bool | List[bool] | Set[int] | None = None):
        """
        Object constructor.

        :param side_length: The length of the sides of the equilateral triangle.
        :param depth: The depth of the equilateral triangle.
        :param center: Whether the triangle must be centered with its point of mass at the origin.
        :param profile_factories: The profile factories to be applied at nodes of the right triangle. When a single
                                  profile factory is given, this profile will be applied at all nodes.
        :param extend_sides_by_eps: Whether to extend sides by eps for a clear overlap.
        """
        EquilateralTriangle.__init__(self,
                                     side_length=side_length,
                                     depth=depth,
                                     center=center,
                                     extend_sides_by_eps=extend_sides_by_eps)
        SmoothPolygonMixin.__init__(self, profile_factories=profile_factories)

# ----------------------------------------------------------------------------------------------------------------------
