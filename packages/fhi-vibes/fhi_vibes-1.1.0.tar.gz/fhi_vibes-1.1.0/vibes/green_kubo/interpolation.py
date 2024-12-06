import numpy as np
import xarray as xr
from scipy.interpolate import LinearNDInterpolator, griddata
from scipy.spatial.qhull import QhullError

from vibes import dimensions, keys
from vibes.dynamical_matrix import DynamicalMatrix
from vibes.helpers import talk
from vibes.helpers.lattice_points import get_unit_grid_extended

_prefix = "gk.interpolation"


def _talk(*args, **kwargs):
    return talk(*args, **kwargs, prefix=_prefix)


def interpolate_to_gamma(
    q_points: np.ndarray,
    array_sq: np.ndarray,
    extend_minus: bool = True,
    tol: float = 1e-9,
) -> np.ndarray:
    """
    Get values at Gamma from interpolating surrounding values

    Args:
    ----
        q_points: the training grid, FIRST q-point is Gamma, [Nq, 3]
        array_sq: array in shape [Ns, Nq] used for interpolating to Gamma
        extend_minus: extend the q-grid to -q using assuming inversion symmetry
        tol: tolerance for wrapping

    Returns:
    -------
        array_s: array with interpolated values at Gamma

    """
    # check if first q-point is gamma
    assert np.linalg.norm(q_points[0]) < tol

    # make sure new points are in [-0.5, 0.5)
    train_qs = q_points[1:]  # (q_points[1:] + 0.5 + tol) % 1 - tol - 0.5
    train_array = array_sq[:, 1:]

    if extend_minus:
        train_qs = np.concatenate([train_qs, -train_qs])
        train_array = np.concatenate([train_array, train_array], axis=1)

    q_gamma = np.zeros(3)

    array_s = np.zeros_like(array_sq[:, 0])
    for ns, l in enumerate(train_array):
        interpolator = LinearNDInterpolator(train_qs, l)
        l_s_at_gamma = float(interpolator(q_gamma))
        array_s[ns] = l_s_at_gamma

    return array_s


def interpolate_to_grid(
    q_points: np.ndarray,
    train_array_sq: np.ndarray,
    train_points: np.ndarray,
    tol: bool = 1e-9,
) -> np.ndarray:
    """
    Interpolate values to new q-grid

    Args:
    ----
        q_points: new q-points [Nq, 3]
        train_array_sq: the training points in [Ns, Nq]
        train_points: training grid, new point must lie in convex hull
        tol: finite zero

    Returns:
    -------
        values from train_array_sq interpolated to q_points

    """
    # make sure new points are in [0, 1]
    new_points = (q_points + tol) % 1 - tol

    grid_interpolators = []
    for l in train_array_sq:
        interpolator = griddata(train_points, l, new_points)
        grid_interpolators.append(interpolator)

    return np.array(grid_interpolators)


def get_interpolation_data(
    dmx: DynamicalMatrix, lifetimes: xr.DataArray, cv: float, nq_max: int = 20
) -> dict:
    """
    interpolate BTE-type thermal conductivity to dense grid

    Args:
    ----
        dmx: dynamical matrix object used for interpolating frequencies etc.
        lifetimes: the lifetimes at commensurate q-points
        cv: heat capacity
        nq_max: interpolate to 3*[nq_max], use as baseline for extrapolating to infinity

    Returns:
    -------
        results dictionary: {
            "interpolation_fit_slope": slope of scaling with 1/nq
            "interpolation_fit_intercept": intercept of linear fit
            "interpolation_fit_stderr": stderr of fit
            "interpolation_correction_factor": K_interpolated = correction_factor * K
            "interpolation_correction_factor_err": error of correction factor
            "interpolation_array": DataArray of interpolated K values
        }

    """
    from scipy.optimize import curve_fit

    from .harmonic import get_kappa

    # define scaled lifetimes
    l_sq = dmx.w2_sq * np.nan_to_num(lifetimes)

    # get value at gamma from interpolating
    try:
        l_sq[:, 0] = interpolate_to_gamma(dmx.q_points, l_sq, extend_minus=True)
    except QhullError:
        _talk("**QhullError  ")
        _talk("**Most likely the sampling of q-points is insufficient in >=1 direction")
        _talk("**Interpolation is not available in this case, sorry!")
        return {}

    _rep = np.array2string(l_sq[:, 0], precision=2)
    _talk(f"Interpolated l_sq at Gamma: {_rep}")

    # create training data on extended unit grid [0, 1]
    train_grid = get_unit_grid_extended(dmx.q_points)
    train_l_sq = l_sq[:, train_grid.map2extended]

    # sanity check that interpolator is idempotent
    kw_train = {
        "train_array_sq": train_l_sq,
        "train_points": train_grid.points_extended,
    }
    l_sq_int = interpolate_to_grid(dmx.q_points, **kw_train)
    assert np.allclose(l_sq, l_sq_int), (l_sq, l_sq_int)

    # get kappa w/o interpolation (same as K_ha_q_symmetrized)
    kappa_ha = get_kappa(dmx.v_sqa_cartesian, tau_sq=lifetimes, cv_sq=cv)

    # interpolate
    nqs = np.arange(4, nq_max + 1, 2)

    Nq_init = len(dmx.q_points)  # number of commensurate q-points
    Ks = np.zeros((len(nqs), 3, 3))
    for ii, nq in enumerate(nqs):
        mesh = (nq, nq, nq)

        # create grid and harmonic solution on grid
        # SZ comment:
        # here we use Gamma centered q mesh for interpolation instead of monkhorst
        # q mesh as described in Knoop PRB 2023.
        # The contribution from q point is not indentical, change from Gamma centered
        # q grid to monkhorst q grid may cause large disagreements at commensurate
        # q points. Using Gamma centered q grid will offer smoother interpolation.
        grid, solution = dmx.get_mesh_and_solution(mesh, reduced=False, monkhorst=False)

        # interpolate scaled lifetimes on irred. grid
        ir_l_int_sq = interpolate_to_grid(q_points=grid.ir.points, **kw_train)

        # scale back to lifetimes
        tau_int_sq = ir_l_int_sq[:, grid.ir.map2full] * solution.w_inv_sq ** 2

        # compute K on new grid, account for change in grid point number
        Nq_eff = len(grid.points) / Nq_init
        KK = get_kappa(solution.v_sqa_cartesian, tau_int_sq, cv) / Nq_eff

        # assign and report: K = tensor, k = scalar
        Ks[ii] = KK
        kk = np.diagonal(KK).mean()
        _talk(f"{nq:3d}, Nq_eff = {Nq_eff:6.2f}, kappa = {kk:.3f} W/mK")

    Ks = xr.DataArray(Ks, dims=("nq", *dimensions.a_b), coords={"nq": nqs})

    # interpolate to infinitely dense grid assuming convergence with 1/nq (Riemann sum)
    # anisotropic extrapolate for each components k_ab
    correction_ab = np.zeros((3, 3))
    correction_ab_stderr = np.zeros((3, 3))
    for _a, _b in np.ndindex(3, 3):
        ks = Ks[:, _a, _b]
        # init linear fit parameters
        p0 = -1, 10
        popt, pcov = curve_fit(
            lambda x, m, y0: m * x + y0, nqs**-1.0, ks, p0, sigma=nqs**-1.0
        )
        perr = np.sqrt(np.diag(pcov))
        m, y0 = popt
        stderr = perr[0]

        k_ha_ab = kappa_ha[_a, _b]  # np.diagonal(kappa_ha).mean()
        nq = len(dmx.q_points) ** (1 / 3)

        correction_ab[_a, _b] = y0 - k_ha_ab
        correction_ab_stderr[_a, _b] = stderr

    k_ha = np.diagonal(kappa_ha).mean()
    correction = np.diagonal(correction_ab).mean()  # -m / nq
    correction_factor = 1 + correction / k_ha
    correction_factor_err = np.diagonal(correction_ab_stderr).mean() / nq / k_ha

    k_ha_int = correction_factor * k_ha

    err_str1 = f"+/- {stderr / nq:.3f}"
    err_str2 = f"+/- {correction_factor_err:.3f}"
    _talk(f"Initial harmonic kappa value:       {k_ha:.3f} W/mK")
    _talk(f"Fit intercept:                      {y0:.3f} W/mK")
    _talk(f"Fit intercept - initial value:      {y0 - k_ha:.3f} {err_str1}  W/mK")
    _talk(f"Interpolated harm. kappa:           {k_ha_int:.3f} {err_str1} W/mK")
    _talk(["Correction^ab: ", *np.array2string(correction_ab, precision=3).split("\n")])
    _talk(f"Correction:                         {correction:.3f} {err_str1} W/mK")
    _talk(f"Correction factor:                  {correction_factor:.3f} {err_str2}")

    # compile results
    dims_w = (dimensions.s, dimensions.q_int)
    dims_q = (dimensions.q_int, dimensions.a)
    dims_a_b = dimensions.a_b
    return {
        keys.interpolation_fit_slope: m,
        keys.interpolation_fit_intercept: y0,
        keys.interpolation_fit_stderr: stderr,
        keys.interpolation_correction: correction,
        keys.interpolation_correction_ab: (dims_a_b, correction_ab),
        keys.interpolation_correction_ab_stderr: (dims_a_b, correction_ab_stderr),
        keys.interpolation_correction_factor: correction_factor,
        keys.interpolation_correction_factor_err: correction_factor_err,
        keys.interpolation_kappa_array: Ks,
        keys.interpolation_q_points: (dims_q, grid.points),
        keys.interpolation_w_sq: (dims_w, solution.w_sq),
        keys.interpolation_tau_sq: (dims_w, tau_int_sq),
    }
