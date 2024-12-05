from dataclasses import dataclass

from super_scad.type import Vector2


@dataclass(frozen=True)
class SmoothProfileParams:
    """
    Dataclass for the parameters for creating a smoothing profile widget.
    """
    # ------------------------------------------------------------------------------------------------------------------
    inner_angle: float
    """
    The inner angle of the vertices at the node. 
    """

    normal_angle: float
    """
    The normal angle of the vertices, i.e., the angle of the vector that lies exactly between the two vertices and with
     origin at the node.
    """

    position: Vector2
    """
    The position of the node.
    """

    side1_is_extended_by_eps: bool = False
    """
    Whether the first side at the node is extended by eps.
    """

    side2_is_extended_by_eps: bool = False
    """
    Whether the second side at the node is extended by eps.
    """

# ----------------------------------------------------------------------------------------------------------------------
