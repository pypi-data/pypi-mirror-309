from super_scad.scad.ArgumentAdmission import ArgumentAdmission
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.util.Radius2Sides4n import Radius2Sides4n
from super_scad_smooth_profile.Rough import Rough
from super_scad_smooth_profile.SmoothProfile import SmoothProfile

from super_scad_cone.SmoothCone import SmoothCone


class SmoothCylinder(ScadWidget):
    """
    Widget for cylinders with smooth edges.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 height: float,
                 radius: float | None = None,
                 diameter: float | None = None,
                 outer_radius: float | None = None,
                 outer_diameter: float | None = None,
                 inner_radius: float | None = None,
                 inner_diameter: float | None = None,
                 center: bool = False,
                 top_inner_profile: SmoothProfile | None = None,
                 top_outer_profile: SmoothProfile | None = None,
                 bottom_outer_profile: SmoothProfile | None = None,
                 bottom_inner_profile: SmoothProfile | None = None,
                 top_extend_by_eps: bool | None = None,
                 outer_extend_by_eps: bool | None = None,
                 bottom_extend_by_eps: bool | None = None,
                 inner_extend_by_eps: bool | None = None,
                 rotate_extrude_angle: float = 360.0,
                 convexity: int | None = None,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 fn4n: bool | None = None):
        """
        Object constructor.

        :param height: The height of the cylinder.
        :param radius: The radius of the cylinder.
        :param diameter: The diameter of the cylinder.
        :param outer_radius: The outer radius of the cylinder.
        :param outer_diameter: The outer diameter at the top of the cylinder.
        :param inner_radius: The inner radius at the top of the cylinder.
        :param inner_diameter: The inner diameter at the top of the cylinder.
        :param center: Whether the cylinder is centered in the z-direction.
        :param top_inner_profile: The profile to be applied at the inner top of the cylinder.
        :param top_outer_profile: The profile to be applied at the outer top of the cylinder.
        :param bottom_outer_profile: The profile to be applied at the outer bottom of the cylinder.
        :param bottom_inner_profile: The profile to be applied at the inner bottom of the cylinder.
        :param top_extend_by_eps: Whether to extend the top of the cylinder by eps for a clear overlap.
        :param outer_extend_by_eps: Whether to extend the outer wall of the cylinder by eps for a clear overlap.
        :param bottom_extend_by_eps: Whether to extend the bottom of the cylinder by eps for a clear overlap.
        :param inner_extend_by_eps: Whether to extend the inner wall of the cylinder by eps for a clear overlap.
        :param rotate_extrude_angle: Specifies the number of degrees to sweep, starting at the positive X axis. The
                                     direction of the sweep follows the Right-Hand Rule, hence a negative angle sweeps
                                     clockwise.
        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line
                          through the child widget.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        :param fn4n: Whether to create a cylinder with a multiple of 4 vertices.
        """
        ScadWidget.__init__(self, args=locals())

        self._height: float = height
        """
        The height of the cylinder.
        """

        self._radius: float | None = radius
        """
        The radius of the top of the cylinder.
        """

        self._diameter: float | None = diameter
        """
        The diameter of the top of the cylinder.
        """

        self._outer_radius: float | None = outer_radius
        """
        The radius of the top of the outer cylinder.
        """

        self._outer_diameter: float | None = outer_diameter
        """
        The diameter of the top of the outer cylinder.
        """

        self._inner_radius: float | None = inner_radius
        """
        The radius of the top of the inner cylinder.
        """

        self._inner_diameter: float | None = inner_diameter
        """
        The diameter of the top of the inner cylinder.
        """

        self._center: bool = center
        """
        Whether the cylinder is centered in the z-direction.
        """

        self._top_inner_profile: SmoothProfile = top_inner_profile or Rough()
        """
        The profile to be applied at the inner top of the cylinder.
        """

        self._top_outer_profile: SmoothProfile = top_outer_profile or Rough()
        """
        The profile to be applied at the outer top of the cylinder.
        """

        self._bottom_outer_profile: SmoothProfile = bottom_outer_profile or Rough()
        """
        The profile to be applied at the outer bottom of the cylinder.
        """

        self._bottom_inner_profile: SmoothProfile = bottom_inner_profile or Rough()
        """
        The profile to be applied at the inner bottom of the cylinder.
        """

        self._top_extend_by_eps: bool = top_extend_by_eps
        """
        Whether to extend the top of the cylinder by eps for a clear overlap.
        """

        self._outer_extend_by_eps: bool = outer_extend_by_eps
        """
        Whether to extend the outer wall of the cylinder by eps for a clear overlap.
        """

        self._bottom_extend_by_eps: bool = bottom_extend_by_eps
        """
        Whether to extend the bottom of the cylinder by eps for a clear overlap.
        """

        self._inner_extend_by_eps: bool = inner_extend_by_eps
        """
        Whether to extend the inner wall of the cylinder by eps for a clear overlap.
        """

        self._rotate_extrude_angle: float = rotate_extrude_angle
        """
        Specifies the number of degrees to sweep, starting at the positive X axis.  The direction of the sweep follows
        the Right-Hand Rule, hence a negative angle sweeps clockwise.
        """

        self._convexity: int | None = convexity
        """
        The convexity of the cylinder.
        """

        self._fa: float | None = fa
        """
        The minimum angle (in degrees) of each fragment.
        """

        self._fs: float | None = fs
        """
        The minimum circumferential length of each fragment.
        """

        self._fn: int | None = fn
        """
        The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        """

        self._fn4n: bool = fn4n
        """
        Whether to create a cylinder with a multiple of 4 vertices.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.
        """
        admission = ArgumentAdmission(self._args)
        admission.validate_exclusive({'radius', 'diameter'},
                                     {'inner_radius', 'outer_radius'},
                                     {'inner_diameter', 'outer_diameter'})
        admission.validate_required({'height'},
                                    {'radius',
                                     'diameter',
                                     'outer_radius',
                                     'outer_diameter'},
                                    {'center'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the cylinder is centered along the z-as.
        """
        return self._center

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_extend_by_eps(self) -> bool:
        """
        Returns whether the top of the cylinder is extended by eps.
        """
        return self._top_extend_by_eps

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def outer_extend_by_eps(self) -> bool:
        """
        Returns whether the outer wall of the cylinder is extended by eps.
        """
        return self._outer_extend_by_eps

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_extend_by_eps(self) -> bool:
        """
        Returns whether the bottom of the cylinder is extended (outwards) by eps.
        """
        return self._bottom_extend_by_eps

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_extend_by_eps(self) -> bool:
        """
        Returns whether the inner wall of the cylinder is extended (inwards) by eps.
        """
        return self._inner_extend_by_eps

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def outer_radius(self) -> float:
        """
        Returns the top outer radius of the cylinder.
        """
        if self._outer_radius is None:
            self._outer_radius = self._radius or \
                                 0.5 * (self._outer_diameter or self._diameter or 0.0)

        return self._outer_radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def outer_diameter(self) -> float:
        """
        Returns the top outer diameter of the cylinder.
        """
        if self._outer_diameter is None:
            self._outer_diameter = self._diameter or \
                                   2.0 * (self._outer_radius or self._radius or 0.0)

        return self._outer_diameter

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_radius(self) -> float:
        """
        Returns the top inner radius of the cylinder.
        """
        if self._inner_radius is None:
            self._inner_radius = 0.5 * (self._inner_diameter or 0.0)

        return self._inner_radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_diameter(self) -> float:
        """
        Returns the top inner diameter of the cylinder.
        """
        if self._inner_diameter is None:
            self._inner_diameter = 2.0 * (self._inner_radius or 0.0)

        return self._inner_diameter

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_inner_profile(self) -> SmoothProfile:
        """
        Returns the top inner profile of the cone.
        """
        return self._top_inner_profile

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_outer_profile(self) -> SmoothProfile:
        """
        Returns the top outer profile of the cone.
        """
        return self._top_outer_profile

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_inner_profile(self) -> SmoothProfile:
        """
        Returns the bottom inner profile of the cone.
        """
        return self._bottom_inner_profile

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_outer_profile(self) -> SmoothProfile:
        """
        Returns the bottom outer profile of the cone.
        """
        return self._bottom_outer_profile

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def height(self) -> float:
        """
        Returns the height of the cone.
        """
        return self._height

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def convexity(self) -> int | None:
        """
        Returns the convexity.
        """
        if self._convexity is None:
            if self.inner_radius != 0.0:
                self._convexity = 2

        return self._convexity

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fa(self) -> float | None:
        """
        Returns the minimum angle (in degrees) of each fragment.
        """
        return self._fa

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fs(self) -> float | None:
        """
        Returns the minimum circumferential length of each fragment.
        """
        return self._fs

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn(self) -> int | None:
        """
        Returns the fixed number of fragments in 360 degrees. Values of 3 or more override $fa and $fs.
        """
        return self._fn

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn4n(self) -> bool:
        """
        Returns whether to create a circle with multiple of 4 vertices.
        """
        return self._fn4n

    # ------------------------------------------------------------------------------------------------------------------
    def real_fn(self, context: Context) -> int | None:
        """
        Returns the real fixed number of fragments in 360 degrees.
        """
        if self._fn4n:
            return Radius2Sides4n.r2sides4n(context, self.outer_radius)

        return self._fn

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def rotate_extrude_angle(self) -> float:
        """
        Returns the number of degrees to sweep, starting at the positive X axis.
        """
        return self._rotate_extrude_angle

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return SmoothCone(height=self.height,
                          top_outer_diameter=self.outer_diameter,
                          top_inner_diameter=self.inner_diameter,
                          bottom_outer_diameter=self.outer_diameter,
                          bottom_inner_diameter=self.inner_diameter,
                          center=self.center,
                          top_inner_profile=self.top_inner_profile,
                          top_outer_profile=self.top_outer_profile,
                          bottom_outer_profile=self.bottom_outer_profile,
                          bottom_inner_profile=self.bottom_inner_profile,
                          top_extend_by_eps=self.top_extend_by_eps,
                          outer_extend_by_eps=self.outer_extend_by_eps,
                          bottom_extend_by_eps=self.bottom_extend_by_eps,
                          inner_extend_by_eps=self.inner_extend_by_eps,
                          rotate_extrude_angle=self.rotate_extrude_angle,
                          convexity=self.convexity,
                          fa=self.fa,
                          fs=self.fs,
                          fn=self.fn,
                          fn4n=self.fn4n)

# ----------------------------------------------------------------------------------------------------------------------
