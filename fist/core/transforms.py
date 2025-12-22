# image array transformation operations

import numpy as np

def apply_transform(arr, T):
    """Apply flip, rotate, negative."""
    out = arr
    if T.get("flip_x"):
        out = np.fliplr(out)
    if T.get("flip_y"):
        out = np.flipud(out)
    k = T.get("rot90", 0) % 4
    if k != 0:
        out = np.rot90(out, k=(-k)%4)
    if T.get("negative"):
        out = 1.0 - out
    return out

