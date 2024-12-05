from abc import ABC, abstractmethod
from typing import Any, Dict

from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget

from super_scad_smooth_profile.SmoothProfileParams import SmoothProfileParams


class SmoothProfileFactory(ABC):
    """
    A smooth profile factory is an abstract base class for smooth profile factories. A smooth profile factory is an
    object that creates a smooth profile SuperSCAD widget given an inner angle, a normal angle, and a position of a
    node and its two vertices, a.k.a., a corner or edge.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def create_smooth_profile(self, *, params: SmoothProfileParams, child: ScadWidget) -> ScadSingleChildParent:
        """
        Returns a smooth profile widget.

        :param params: The parameters for the smooth profile widget.
        :param child: The child object on which the smoothing must be applied.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def offset1(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the first vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def offset2(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the second vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
