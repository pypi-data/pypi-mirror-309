from abc import ABC
from typing import List

from super_scad.d2.helper.PolygonSideExtender import PolygonSideExtender
from super_scad.d2.PolygonMixin import PolygonMixin
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad_smooth_profile.RoughFactory import RoughFactory
from super_scad_smooth_profile.SmoothProfileFactory import SmoothProfileFactory
from super_scad_smooth_profile.SmoothProfileParams import SmoothProfileParams

from super_scad_polygon.helper.SmoothPolygonSideExtender import SmoothPolygonSideExtender


# class SmoothPolygonMixin(PolygonMixin, ScadWidget, ABC):
class SmoothPolygonMixin(ABC):
    """
    A widget for polygons with smooth corners.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, profile_factories: SmoothProfileFactory | List[SmoothProfileFactory] | None):
        """
        Object constructor.

        :param profile_factories: The profile factories to be applied at nodes of the polygon. When a single profile
                                  factory is given, this profile will be applied at all nodes.
        """
        self._profile_factories = profile_factories
        """
        The profile factories to be applied at nodes of the polygon.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def profile_factories(self) -> List[SmoothProfileFactory]:
        """
        Returns the list of smooth profile factories.
        """
        if isinstance(self._profile_factories, SmoothProfileFactory):
            self._profile_factories = [self._profile_factories for _ in range(self.sides)]

        elif isinstance(self._profile_factories, List):
            if len(self._profile_factories) < self.sides:
                self._profile_factories += [RoughFactory() for _ in range(len(self._profile_factories), self.sides)]

        elif self._profile_factories is None:
            self._profile_factories = [RoughFactory() for _ in range(self.sides)]

        else:
            raise ValueError(f'Parameter profile_factories SmoothProfileFactory, '
                             f', a list of SmoothProfileFactory or None, got {type(self._profile_factories)}')

        return self._profile_factories

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        polygon = PolygonMixin.build(self, context)

        nodes = self.nodes
        inner_angles = self.inner_angles(context)
        normal_angles = self.normal_angles(context)
        profile_factories = self.profile_factories
        for index in range(len(nodes)):
            profile = profile_factories[index]
            polygon = profile.create_smooth_profile(params=SmoothProfileParams(inner_angle=inner_angles[index],
                                                                               normal_angle=normal_angles[index],
                                                                               position=nodes[index]),
                                                    child=polygon)

        return polygon

    # ------------------------------------------------------------------------------------------------------------------
    def _create_polygon_side_extender(self) -> PolygonSideExtender:
        """
        Returns a polygon side extender that extends this polygon.
        """
        return SmoothPolygonSideExtender(self.profile_factories)

# ----------------------------------------------------------------------------------------------------------------------
