from super_scad.scad.Context import Context
from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget


class Rough(ScadSingleChildParent):
    """
    Applies no finish to the edges at a node.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, child: ScadWidget):
        """
        Object constructor.

        :param child: The child object which will be left rough.
        """
        ScadSingleChildParent.__init__(self, args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return self.child

# ----------------------------------------------------------------------------------------------------------------------
