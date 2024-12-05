import math

from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.scad.ScadWidget import ScadWidget
from super_scad_smooth_profile.SmoothProfile import SmoothProfile
from super_scad_smooth_profile.SmoothProfileParams import SmoothProfileParams

from super_scad_smooth_profiles.ExteriorFilletWidget import ExteriorFilletWidget
from super_scad_smooth_profiles.InteriorFilletWidget import InteriorFilletWidget


class Fillet(SmoothProfile):
    """
    A profile that produces fillet smoothing profile widgets.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, radius: float, side: int | None = None):
        """
        Object constructor.

        :param radius: The radius of the fillet.
        :param side: The edge on which the exterior fillet must be applied.
        """

        self._radius: float = radius
        """
        The radius of the fillet.
        """

        self._side: int | None = side
        """
        The edge on which the exterior fillet must be applied. 
        """

    # ------------------------------------------------------------------------------------------------------------------
    def offset1(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the first vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        if self._side is None:
            if self._radius > 0.0 and inner_angle < 180.0:
                # The corner is convex.
                alpha = math.radians(inner_angle) / 2.0

                return self._radius * math.cos(alpha) / math.sin(alpha)

            if self._radius > 0.0 and inner_angle > 180.0:
                # The corner is concave.
                alpha = math.radians(360.0 - inner_angle) / 2.0

                return self._radius * math.cos(alpha) / math.sin(alpha)

            if self._radius < 0.0:
                # Negative radius.
                return -self._radius

            return 0.0

        if self._side == 1:
            # The corner is convex.
            if self._radius > 0.0 and inner_angle < 180.0:
                # The corner is convex.
                alpha = math.radians(inner_angle) / 2.0

                return self._radius * math.cos(alpha) / math.sin(alpha)

            if self._radius > 0.0 and inner_angle > 180.0:
                # The corner is concave.
                print('Warning: Not possible to apply an exterior fillet on a concave corner.')

                return 0.0

            if self._radius < 0.0:
                # Negative radius.
                return -self._radius

            return 0.0

        if self._side == 2:
            return 0.0

        raise ValueError(f'Side must be 1 or 2, got {self._side}.')

    # ------------------------------------------------------------------------------------------------------------------
    def offset2(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the second vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        if self._side is None:
            if self._radius > 0.0 and inner_angle < 180.0:
                # The corner is convex.
                alpha = math.radians(inner_angle) / 2.0

                return self._radius * math.cos(alpha) / math.sin(alpha)

            if self._radius > 0.0 and inner_angle > 180.0:
                # The corner is concave.
                alpha = math.radians(360.0 - inner_angle) / 2.0

                return self._radius * math.cos(alpha) / math.sin(alpha)

            if self._radius < 0.0:
                # Negative radius.
                return -self._radius

            return 0.0

        if self._side == 2:
            if self._radius > 0.0 and inner_angle < 180.0:
                # The corner is convex.
                alpha = math.radians(inner_angle) / 2.0

                return self._radius * math.cos(alpha) / math.sin(alpha)

            if self._radius > 0.0 and inner_angle > 180.0:
                # The corner is concave.
                print('Warning: Not possible to apply an exterior fillet on a concave corner.')

                return 0.0

            if self._radius < 0.0:
                # Negative radius.
                return -self._radius

            return 0.0

        if self._side == 1:
            return 0.0

        raise ValueError(f'Side must be 1 or 2, got {self._side}.')

    # ------------------------------------------------------------------------------------------------------------------
    def create_smooth_profile(self, *, params: SmoothProfileParams, child: ScadWidget) -> ScadSingleChildParent:
        """
        Returns a smoothing profile widget creating a fillet.

        :param params: The parameters for the smooth profile widget.
        :param child: The child object on which the smoothing must be applied.
        """
        if self._side is None:
            return InteriorFilletWidget(radius=self._radius,
                                        inner_angle=params.inner_angle,
                                        normal_angle=params.normal_angle,
                                        position=params.position,
                                        child=child)

        return ExteriorFilletWidget(radius=self._radius,
                                    side=self._side,
                                    inner_angle=params.inner_angle,
                                    normal_angle=params.normal_angle,
                                    position=params.position,
                                    side1_is_extended_by_eps=params.side1_is_extended_by_eps,
                                    side2_is_extended_by_eps=params.side2_is_extended_by_eps,
                                    child=child)

# ----------------------------------------------------------------------------------------------------------------------
