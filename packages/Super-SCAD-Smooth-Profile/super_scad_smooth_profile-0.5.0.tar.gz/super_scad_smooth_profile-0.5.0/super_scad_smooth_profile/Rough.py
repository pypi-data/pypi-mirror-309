from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget

from super_scad_smooth_profile.RoughWidget import RoughWidget
from super_scad_smooth_profile.SmoothProfile import SmoothProfile
from super_scad_smooth_profile.SmoothProfileParams import SmoothProfileParams


class Rough(SmoothProfile):
    """
    A profile that produces rough smoothing profile widgets.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def create_smooth_profile(self, *, params: SmoothProfileParams, child: ScadWidget) -> ScadSingleChildParent:
        """
        Returns a smooth profile widget.

        :param params: The parameters for the smooth profile widget.
        :param child: The child object on which the smoothing must be applied.
        """
        return RoughWidget(child=child)

    # ------------------------------------------------------------------------------------------------------------------
    def offset1(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the first vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        return 0.0

    # ------------------------------------------------------------------------------------------------------------------
    def offset2(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the second vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        return 0.0

# ----------------------------------------------------------------------------------------------------------------------
