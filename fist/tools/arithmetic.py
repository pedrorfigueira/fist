# simple arithmetic functions for FITS image arrays

import numpy as np

def compute_arithmetic(arr1, arr2, op):
    if arr1.shape != arr2.shape:
        return None, False
    with np.errstate(divide='ignore', invalid='ignore'):
        if op == "+":
            out = arr1 + arr2
        elif op == "-":
            out = arr1 - arr2
        elif op in ("×", "x", "*"):
            out = arr1 * arr2
        elif op == "/":
            out = arr1 / arr2
        else:
            out = arr1.copy()
    return out, not np.isfinite(out).all()

