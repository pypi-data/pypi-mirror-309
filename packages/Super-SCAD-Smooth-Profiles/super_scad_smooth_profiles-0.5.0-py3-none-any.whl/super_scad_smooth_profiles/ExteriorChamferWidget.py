import math

from super_scad.boolean.Union import Union
from super_scad.d2.Polygon import Polygon
from super_scad.scad.Context import Context
from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Translate2D import Translate2D
from super_scad.type import Vector2
from super_scad.type.Angle import Angle


class ExteriorChamferWidget(ScadSingleChildParent):
    """
    Applies an exterior chamfer to an edge at a node.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 skew_length: float | None = None,
                 skew_height: float | None = None,
                 side: int,
                 inner_angle: float,
                 normal_angle: float,
                 position: Vector2,
                 side1_is_extended_by_eps: bool,
                 side2_is_extended_by_eps: bool,
                 child: ScadWidget):
        """
        Object constructor.

        :param skew_length: The length of the skew side of the chamfer.
        :param skew_height: The height of the chamfer, measured perpendicular for the skew size to the node.
        :param side: The edge on which the exterior chamfer must be applied.
        :param inner_angle: Inner angle between the vertices.
        :param normal_angle: The normal angle of the vertices, i.e., the angle of the vector that lies exactly between
                             the two vertices and with origin at the node.
        :param side1_is_extended_by_eps: Whether the first side is extended by eps.
        :param side2_is_extended_by_eps: Whether the second side is extended by eps.
        :param child: The child object on which the fillet is applied.
        """
        ScadSingleChildParent.__init__(self, args=locals(), child=child)

        self._skew_length = skew_length
        """
        The length of the skew side of the chamfer.
        """

        self._skew_height = skew_height
        """
        The height of the chamfer, measured perpendicular for the skew size to the node.
        """

        self._side: float = side
        """
        The edge on which the exterior chamfer must be applied. 
        """

        self._inner_angle: float = Angle.normalize(inner_angle)
        """
        The inner angle between the vertices at the node.
        """

        self._normal_angle: float = Angle.normalize(normal_angle)
        """
        The normal angle of the vertices at the node.
        """

        self._position: Vector2 = position
        """
        The position of the node.
        """

        self._side1_is_extended_by_eps = side1_is_extended_by_eps
        """
        Whether the first side is extended by eps.
        """

        self._side2_is_extended_by_eps = side2_is_extended_by_eps
        """
        Whether the second side is extended by eps.
        """

        self._validate_arguments()

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        """
        Validates the arguments supplied to the constructor of this profile.
        """
        # admission = ArgumentAdmission(self._args)
        # admission.validate_exclusive({'skew_length'}, {'skew_height'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def skew_height(self) -> float:
        """
        The skew_height of the chamfer, measured perpendicular for the skew size to the node.
        """
        if self._skew_height is None:
            outer_angle = 180.0 - self._inner_angle
            self._skew_height = 0.5 * self.skew_length / math.tan(math.radians(0.5 * outer_angle))

        return self._skew_height

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def skew_length(self) -> float:
        """
        The length of the skew side of the chamfer.
        """
        if self._skew_length is None:
            outer_angle = 180.0 - self._inner_angle
            self._skew_length = 2.0 * self.skew_height * math.tan(math.radians(0.5 * outer_angle))

        return self._skew_length

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        if self.skew_length > 0.0:
            if self._side == 1:
                polygon = self._build_polygon(self._normal_angle,
                                              True,
                                              self._side2_is_extended_by_eps)

                return Union(children=[self.child, polygon])

            if self._side == 2:
                polygon = self._build_polygon(Angle.normalize(self._normal_angle - 180.0),
                                              self._side1_is_extended_by_eps,
                                              True)

                return Union(children=[self.child, polygon])

            raise ValueError(f'Side must be 1 or 2, got {self._side}.')

        return self.child

    # ------------------------------------------------------------------------------------------------------------------
    def _build_polygon(self,
                       normal_angle: float,
                       extent_by_eps0: bool,
                       extent_by_eps2: bool) -> ScadWidget:
        """
        Returns a masking polygon.

        :param normal_angle: The normal angle of the vertices at the node.
        """
        p2 = Vector2.from_polar_coordinates(self.skew_height, normal_angle - 90.0) + \
             Vector2.from_polar_coordinates(0.5 * self.skew_length, normal_angle)
        p3 = p2 + Vector2.from_polar_coordinates(self.skew_length, normal_angle - 180.0)

        return Translate2D(vector=self._position,
                           child=Polygon(points=[Vector2.origin, p2, p3],
                                         extend_sides_by_eps=[extent_by_eps0, False, extent_by_eps2]))

# ----------------------------------------------------------------------------------------------------------------------
