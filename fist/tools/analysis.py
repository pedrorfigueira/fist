# analysis tool

import numpy as np

from astropy.io import fits

from scipy.ndimage import map_coordinates

# Cuts 

def compute_diagonal_cut(arr, x1, y1, x2, y2, npts=500):
    xs = np.linspace(x1, x2, npts)
    ys = np.linspace(y1, y2, npts)
    coords = np.vstack([ys, xs])  # (row=y, col=x)
    vals = map_coordinates(arr, coords, order=1, mode="nearest")
    dist = np.linspace(0, np.hypot(x2-x1, y2-y1), npts)
    return dist, vals

def update_cut_plot(arr, x1, y1, x2, y2, cut_source):
    if arr is None:
        cut_source.data=dict(x=[],y=[])
        return
    h,w = arr.shape
    x1 = np.clip(x1, 0, w-1)
    x2 = np.clip(x2, 0, w-1)
    y1 = np.clip(y1, 0, h-1)
    y2 = np.clip(y2, 0, h-1)
    dist, vals = compute_diagonal_cut(arr, x1, y1, x2, y2)
    cut_source.data = dict(x=dist, y=vals)

# Region

def compute_region_stats(arr, mask):
    """
    Return a two-row aligned monospace table inside a Markdown code block.
    """

    data = arr[mask]

    # Empty region
    if data.size == 0:
        table = (
            "```\n"
            "Count     Sum     |  Mean      Std      |  Min      Median    Max\n"
            "0         0       |    -         -      |    -        -        -\n"
            "```"
        )
        return table

    # Compute numbers
    N = data.size
    S = np.sum(data)
    mean = np.mean(data)
    std  = np.std(data)
    vmin = np.min(data)
    med  = np.median(data)
    vmax = np.max(data)

    # Format with fixed-width columns using Python formatting
    header = (
        "Count     Sum       |  Mean       Std       |  Min        Median     Max"
    )

    values = (
        f"{N:<9d} "
        f"{S:<9.4g} |  "
        f"{mean:<9.4g}  "
        f"{std:<9.4g} |  "
        f"{vmin:<9.4g}  "
        f"{med:<9.4g}  "
        f"{vmax:<9.4g}"
    )

    # Wrap in a Markdown code block so spacing is preserved
    table = f"```\n{header}\n{values}\n```"

    return table

