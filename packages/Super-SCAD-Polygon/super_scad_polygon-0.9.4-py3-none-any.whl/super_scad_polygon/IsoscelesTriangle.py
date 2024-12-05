import math
from typing import List, Set

from super_scad.d2.PolygonMixin import PolygonMixin
from super_scad.scad.ArgumentAdmission import ArgumentAdmission
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2

from super_scad_polygon.TriangleMixin import TriangleMixin


class IsoscelesTriangle(TriangleMixin, PolygonMixin, ScadWidget):
    """
    Widget for isosceles triangles.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 width: float,
                 isosceles_length: float | None = None,
                 depth: float | None = None,
                 center: bool = False,
                 extend_sides_by_eps: bool | List[bool] | Set[int] | None = None):
        """
        Object constructor.

        :param width: The length of the base of the isosceles triangle.
        :param isosceles_length: The length of the isosceles sides of the isosceles triangle.
        :param depth: The depth of the isosceles triangle.
        :param center: Whether the triangle must be centered with its point of mass at the origin.
        :param extend_sides_by_eps: Whether to extend sides by eps for a clear overlap.
        """
        ScadWidget.__init__(self, args=locals())
        PolygonMixin.__init__(self, extend_sides_by_eps=extend_sides_by_eps)
        TriangleMixin.__init__(self, center=center)

        self._width: float = width
        """
        The length of the base of the isosceles triangle.
        """

        self._isosceles_length: float | None = isosceles_length
        """
        The length of the isosceles sides of the isosceles triangle.
        """

        self._depth: float | None = depth
        """        
        The depth of the isosceles triangle.
        """

        self._validate_arguments()

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.
        """
        admission = ArgumentAdmission(self._args)
        admission.validate_exclusive({'isosceles_length'}, {'depth'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def width(self) -> float:
        """
        Returns the width of this isosceles triangle.
        """
        return self._width

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def isosceles_length(self) -> float:
        """
        Returns length of the isosceles sides of the isosceles triangle.
        """
        if self._isosceles_length is None:
            self._isosceles_length = math.sqrt(self._depth ** 2 + 0.25 * self._width ** 2)

        return self._isosceles_length

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def depth(self) -> float:
        """
        Returns the depth of this equilateral triangle.
        """
        if self._depth is None:
            self._depth = math.sqrt(self._isosceles_length ** 2 - 0.25 * self._width ** 2)

        return self._depth

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def _raw_nodes(self) -> List[Vector2]:
        """
        Returns the nodes of this right triangle.
        """
        return [Vector2.origin, Vector2(0.5 * self.width, self.depth), Vector2(self.width, 0.0)]

# ----------------------------------------------------------------------------------------------------------------------
