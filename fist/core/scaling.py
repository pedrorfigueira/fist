# scaling for image displays

import numpy as np


def percentile_clip(arr, pmin, pmax, gamma, stretch="linear", contrast=1.0):
    a = np.array(arr, dtype=float)
    if np.isnan(a).all():
        return a

    good = a[np.isfinite(a)]
    if good.size == 0:
        return a

    # Percentile-based normalization limits
    lo = np.percentile(good, pmin)
    hi = np.percentile(good, pmax)

    # Linear rescaling to [0, 1]
    scaled = (a - lo) / (hi - lo) if hi > lo else a - lo
    scaled = np.clip(scaled, 0, 1)

    # Optional non-linear stretch for display
    if stretch == "log":
        scaled = np.log1p(9*scaled)/np.log1p(9)
    elif stretch == "sqrt":
        scaled = np.sqrt(scaled)
    elif stretch == "arcsinh":
        scaled = np.arcsinh(5*scaled) / np.arcsinh(5)
    elif stretch == "zscale":
        # Approximate zscale stretch around median ± 1.5σ
        med = np.nanmedian(scaled)
        std = np.nanstd(scaled)
        lo2 = med - 1.5*std
        hi2 = med + 1.5*std
        scaled = np.clip((scaled - lo2)/(hi2-lo2), 0, 1)

    # Contrast adjustment around mid-gray
    if contrast != 1.0:
        scaled = (scaled-0.5)*contrast + 0.5
        scaled = np.clip(scaled, 0, 1)

    if gamma != 1.0:
        scaled = scaled**(1.0/gamma)

    return scaled

