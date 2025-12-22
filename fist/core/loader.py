# FITS file loader utilities
# Provides file fetching, header access, and image extraction helpers

import glob
from pathlib import Path
import numpy as np
from astropy.io import fits

def find_instrument_files(folder, filetype, instrument):
    """
    Return a sorted list of files matching the instrument-defined patterns
    for a given file type within a folder.
    """
    folder = Path(folder)
    patterns = instrument["filetypes"]

    if filetype not in patterns:
        raise ValueError(
            f"Unknown filetype '{filetype}'. "
            f"Available types: {list(patterns.keys())}"
        )

    pattern = patterns[filetype]

    # Allow single pattern or list of patterns
    if isinstance(pattern, str):
        pattern = [pattern]

    files = []
    for pat in pattern:
        files.extend(glob.glob(str(folder / pat)))

    return sorted(files)


def safe_get_header_value(fn, key):
    try:
        hdr = fits.getheader(fn, 0, memmap=False)
        return hdr.get(key)
    except Exception:
        return None

def scan_image_extensions(fn):
    """
    Return names of FITS extensions containing 2D or 3D image data.
    """
    extnames=[]
    try:
        with fits.open(fn, memmap=False) as hdul:
            for hdu in hdul:
                data = hdu.data
                if isinstance(data, np.ndarray) and data.ndim in (2, 3):
                    # ext named as PRIMARY if not named
                    name = hdu.name if hdu.name else "PRIMARY"
                    extnames.append(name)
    except Exception:
        pass
    return extnames

def load_image_slice(fn, extname, src_idx):
    """
    Load a 2D image from a FITS extension.
    For 3D data cubes, returns the selected slice index.
    """
    try:
        from astropy.io import fits
        with fits.open(fn, memmap=False) as hdul:
            hdu = None
            for h in hdul:
                if h.name == extname:
                    hdu = h
                    break
            if h is None:
                return None
            arr = np.asarray(hdu.data, dtype=float)

            # 2D image
            if arr.ndim == 2:
                return arr

            # 3D cube: return selected slice
            if arr.ndim == 3:
                if src_idx is None:
                    src_idx = 0
                if 0 <= src_idx < arr.shape[0]:
                    return arr[src_idx,:,:]
    except Exception:
        return None

