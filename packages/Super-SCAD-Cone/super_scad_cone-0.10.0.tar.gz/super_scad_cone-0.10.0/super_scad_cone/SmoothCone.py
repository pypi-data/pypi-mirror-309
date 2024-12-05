from super_scad.d3.RotateExtrude import RotateExtrude
from super_scad.scad.ArgumentAdmission import ArgumentAdmission
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2
from super_scad.util.Radius2Sides4n import Radius2Sides4n
from super_scad_polygon.SmoothPolygon import SmoothPolygon
from super_scad_smooth_profile.Rough import Rough
from super_scad_smooth_profile.SmoothProfile import SmoothProfile


class SmoothCone(ScadWidget):
    """
    Widget for cones with smooth edges.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 height: float,
                 top_radius: float | None = None,
                 top_diameter: float | None = None,
                 top_outer_radius: float | None = None,
                 top_outer_diameter: float | None = None,
                 top_inner_radius: float | None = None,
                 top_inner_diameter: float | None = None,
                 bottom_radius: float | None = None,
                 bottom_diameter: float | None = None,
                 bottom_outer_radius: float | None = None,
                 bottom_outer_diameter: float | None = None,
                 bottom_inner_radius: float | None = None,
                 bottom_inner_diameter: float | None = None,
                 center: bool = False,
                 top_inner_profile: SmoothProfile | None = None,
                 top_outer_profile: SmoothProfile | None = None,
                 bottom_outer_profile: SmoothProfile | None = None,
                 bottom_inner_profile: SmoothProfile | None = None,
                 top_extend_by_eps: bool = False,
                 outer_extend_by_eps: bool = False,
                 bottom_extend_by_eps: bool = False,
                 inner_extend_by_eps: bool = False,
                 rotate_extrude_angle: float = 360.0,
                 convexity: int | None = None,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 fn4n: bool = False):
        """
        Object constructor.

        :param height: The height of the cone.
        :param top_radius: The radius at the top of the cone.
        :param top_diameter: The diameter at the top of the cone.
        :param top_outer_radius: The radius at the top of the outer cone.
        :param top_outer_diameter: The diameter at the top of the outer cone.
        :param top_inner_radius: The radius at the top of the inner cone.
        :param top_inner_diameter: The diameter at the top of the inner cone.
        :param bottom_radius: The radius at the bottom of the cone.
        :param bottom_diameter: The diameter at the bottom of the cone.
        :param bottom_outer_radius: The radius at the bottom of the outer cone.
        :param bottom_outer_diameter: The diameter at the bottom of the outer cone.
        :param bottom_inner_radius: The radius at the bottom of the inner cone.
        :param bottom_inner_diameter: The diameter at the bottom of the inner cone.
        :param center: Whether the cylinder is centered in the z-direction.
        :param top_inner_profile: The profile to be applied at the inner top of the cone.
        :param top_outer_profile: The profile to be applied at the outer top of the cone.
        :param bottom_outer_profile: The profile to be applied at the outer bottom of the cone.
        :param bottom_inner_profile: The profile to be applied at the inner bottom of the cone.
        :param top_extend_by_eps: Whether to extend the top of the cone by eps for a clear overlap.
        :param outer_extend_by_eps: Whether to extend the outer wall of the cone by eps for a clear overlap.
        :param bottom_extend_by_eps: Whether to extend the bottom of the cone by eps for a clear overlap.
        :param inner_extend_by_eps: Whether to extend the inner wall of the cone by eps for a clear overlap.
        :param rotate_extrude_angle: Specifies the number of degrees to sweep, starting at the positive X axis. The
                                     direction of the sweep follows the Right-Hand Rule, hence a negative angle sweeps
                                     clockwise.
        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line
                          through the child widget.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        :param fn4n: Whether to create a cone with a multiple of 4 vertices.
        """
        ScadWidget.__init__(self, args=locals())

        self._height: float = height
        """
        The height of the cone.
        """

        self._top_radius: float | None = top_radius
        """
        The radius of the top of the cone.
        """

        self._top_diameter: float | None = top_diameter
        """
        The diameter of the top of the cone.
        """

        self._top_outer_radius: float | None = top_outer_radius
        """
        The radius of the top of the outer cone.
        """

        self._top_outer_diameter: float | None = top_outer_diameter
        """
        The diameter of the top of the outer cone.
        """

        self._top_inner_radius: float | None = top_inner_radius
        """
        The radius of the top of the inner cone.
        """

        self._top_inner_diameter: float | None = top_inner_diameter
        """
        The diameter of the top of the inner cone.
        """

        self._bottom_radius: float | None = bottom_radius
        """
        The radius of the bottom of the cone.
        """

        self._bottom_diameter: float | None = bottom_diameter
        """
        The diameter of the bottom of the cone.
        """

        self._bottom_outer_radius: float | None = bottom_outer_radius
        """
        The radius of the bottom of the outer cone.
        """

        self._bottom_outer_diameter: float | None = bottom_outer_diameter
        """
        The diameter of the bottom of the outer cone.
        """

        self._bottom_inner_radius: float | None = bottom_inner_radius
        """
        The radius of the bottom of the inner cone.
        """

        self._bottom_inner_diameter: float | None = bottom_inner_diameter
        """
        The diameter of the bottom of the inner cone.
        """

        self._center: bool = center
        """
        Whether the cylinder is centered in the z-direction.
        """

        self._top_inner_profile: SmoothProfile = top_inner_profile or Rough()
        """
        The profile to be applied at the inner top of the cone.
        """

        self._top_outer_profile: SmoothProfile = top_outer_profile or Rough()
        """
        The profile to be applied at the outer top of the cone.
        """

        self._bottom_outer_profile: SmoothProfile = bottom_outer_profile or Rough()
        """
        The profile to be applied at the outer bottom of the cone.
        """

        self._bottom_inner_profile: SmoothProfile = bottom_inner_profile or Rough()
        """
        The profile to be applied at the inner bottom of the cone.
        """

        self._top_extend_by_eps: bool = top_extend_by_eps
        """
        Whether to extend the top of the cone by eps for a clear overlap.
        """

        self._outer_extend_by_eps: bool = outer_extend_by_eps
        """
        Whether to extend the outer wall of the cone by eps for a clear overlap.
        """

        self._bottom_extend_by_eps: bool = bottom_extend_by_eps
        """
        Whether to extend the bottom of the cone by eps for a clear overlap.
        """

        self._inner_extend_by_eps: bool = inner_extend_by_eps
        """
        Whether to extend the inner wall of the cone by eps for a clear overlap.
        """

        self._rotate_extrude_angle: float = rotate_extrude_angle
        """
        Specifies the number of degrees to sweep, starting at the positive X axis.  The direction of the sweep follows
        the Right-Hand Rule, hence a negative angle sweeps clockwise.
        """

        self._convexity: int | None = convexity
        """
        The convexity of the cone.
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
        Whether to create a cone with a multiple of 4 vertices.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.
        """
        admission = ArgumentAdmission(self._args)
        admission.validate_exclusive({'top_radius'},
                                     {'top_diameter'},
                                     {'top_inner_radius', 'top_outer_radius'},
                                     {'top_inner_diameter', 'top_outer_diameter'})
        admission.validate_exclusive({'bottom_radius'},
                                     {'bottom_diameter'},
                                     {'bottom_inner_radius', 'bottom_outer_radius'},
                                     {'bottom_inner_diameter', 'bottom_outer_diameter'})
        admission.validate_required({'height'},
                                    {'bottom_radius',
                                     'bottom_diameter',
                                     'bottom_outer_radius',
                                     'bottom_outer_diameter'},
                                    {'top_radius',
                                     'top_diameter',
                                     'top_outer_radius',
                                     'top_outer_diameter'},
                                    {'center'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the cone is centered along the z-as.
        """
        return self._center

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_extend_by_eps(self) -> bool:
        """
        Returns whether the top of the cone is extended by eps.
        """
        return self._top_extend_by_eps

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def outer_extend_by_eps(self) -> bool:
        """
        Returns whether the outer wall of the cone is extended by eps.
        """
        return self._outer_extend_by_eps

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_extend_by_eps(self) -> bool:
        """
        Returns whether the bottom of the cone is extended (outwards) by eps.
        """
        return self._bottom_extend_by_eps

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_extend_by_eps(self) -> bool:
        """
        Returns whether the inner wall of the cone is extended (inwards) by eps.
        """
        return self._inner_extend_by_eps

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_outer_radius(self) -> float:
        """
        Returns the top outer radius of the cone.
        """
        if self._top_outer_radius is None:
            self._top_outer_radius = self._top_radius or \
                                     0.5 * (self._top_outer_diameter or self._top_diameter or 0.0)

        return self._top_outer_radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_outer_diameter(self) -> float:
        """
        Returns the top outer diameter of the cone.
        """
        if self._top_outer_diameter is None:
            self._top_outer_diameter = self._top_diameter or \
                                       2.0 * (self._top_outer_radius or self._top_radius or 0.0)

        return self._top_outer_diameter

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_inner_radius(self) -> float:
        """
        Returns the top inner radius of the cone.
        """
        if self._top_inner_radius is None:
            self._top_inner_radius = 0.5 * (self._top_inner_diameter or 0.0)

        return self._top_inner_radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_inner_diameter(self) -> float:
        """
        Returns the top inner diameter of the cone.
        """
        if self._top_inner_diameter is None:
            self._top_inner_diameter = 2.0 * (self._top_inner_radius or 0.0)

        return self._top_inner_diameter

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_outer_radius(self) -> float:
        """
        Returns the bottom outer radius of the cone.
        """
        if self._bottom_outer_radius is None:
            self._bottom_outer_radius = self._bottom_radius or \
                                        0.5 * (self._bottom_outer_diameter or self._bottom_diameter or 0.0)

        return self._bottom_outer_radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_outer_diameter(self) -> float:
        """
        Returns the bottom outer diameter of the cone.
        """
        if self._bottom_outer_diameter is None:
            self._bottom_outer_diameter = self._bottom_diameter or \
                                          2.0 * (self._bottom_outer_radius or self._bottom_radius or 0.0)

        return self._bottom_outer_diameter

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_inner_radius(self) -> float:
        """
        Returns the bottom inner radius of the cone.
        """
        if self._bottom_inner_radius is None:
            self._bottom_inner_radius = 0.5 * (self._bottom_inner_diameter or 0.0)

        return self._bottom_inner_radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_inner_diameter(self) -> float:
        """
        Returns the bottom inner diameter of the cone.
        """
        if self._bottom_inner_diameter is None:
            self._bottom_inner_diameter = 2.0 * (self._bottom_inner_radius or 0.0)

        return self._bottom_inner_diameter

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
            if self.top_inner_radius != 0.0 or self.bottom_inner_radius != 0.0:
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
            return Radius2Sides4n.r2sides4n(context, max(self.bottom_outer_radius, self.top_outer_radius))

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
        top_height = self.height / 2.0 if self.center else self.height
        bottom_height = -self.height / 2.0 if self.center else 0.0
        top_inner_radius = self.top_inner_radius
        bottom_inner_radius = self.bottom_inner_radius
        if self.inner_extend_by_eps:
            top_inner_radius = max(top_inner_radius, context.eps)
            bottom_inner_radius = max(bottom_inner_radius, context.eps)

        profile = SmoothPolygon(primary=[Vector2(top_inner_radius, top_height),
                                         Vector2(self.top_outer_radius, top_height),
                                         Vector2(self.bottom_outer_radius, bottom_height),
                                         Vector2(bottom_inner_radius, bottom_height)],
                                profiles=[self.top_inner_profile,
                                          self.top_outer_profile,
                                          self.bottom_outer_profile,
                                          self.bottom_inner_profile],
                                extend_sides_by_eps=[self.top_extend_by_eps,
                                                     self.outer_extend_by_eps,
                                                     self.bottom_extend_by_eps,
                                                     self.inner_extend_by_eps],
                                convexity=self.convexity)

        return RotateExtrude(angle=self.rotate_extrude_angle,
                             convexity=self.convexity,
                             fa=self.fa,
                             fs=self.fs,
                             fn=self.real_fn(context),
                             child=profile)

# ----------------------------------------------------------------------------------------------------------------------
