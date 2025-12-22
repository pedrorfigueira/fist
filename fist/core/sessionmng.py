# session / folder management utilities

from pathlib import Path

from fist.core.loader import find_instrument_files, safe_get_header_value, scan_image_extensions, load_image_slice

# -------------------------------
# Folder scanning helpers
# -------------------------------

def scan_folder_impl(w, instr, state):
    folder = w["input_dir"].value
    ftype = w["filetype"].value
    path = Path(folder).expanduser()

    if not path.exists() or not path.is_dir():
        w["info_state"].object = f"Folder not found: {path}"
        return

    files = find_instrument_files(path, ftype, instr)
    if not files:
        w["info_state"].object = f"No {ftype} files in {path}"
        return

    files = [str(Path(f).resolve()) for f in files]

    kw = w["sort_key"].value.strip()

    def sort_key_func(f):
        v = safe_get_header_value(f, kw)
        if v is None:
            return float("inf")  # push files without keyword to bottom
        # Try numeric sorting first
        try:
            return float(v)
        except:
            return str(v)

    state["file_list"] = sorted(files, key=sort_key_func)

    w["file_sel"].options = {
        Path(f).name: f
        for f in state["file_list"]
    }

    if state["file_list"]:
        w["file_sel"].value = state["file_list"][0]

    w["file_idx"].start = 1
    w["file_idx"].end = len(state["file_list"])
    w["file_idx"].value = 1

    state["ext_cache"].clear()
    for f in state["file_list"][:100]:
        state["ext_cache"][f] = scan_image_extensions(f)

    # arith second-file: keep "None" plus full paths
    w["arith_file"].options = {"None": "None"} | {
        Path(f).name: f
        for f in state["file_list"]
    }
    w["arith_file"].value = "None"

    w["info_state"].object = f"Found {len(files)} files (sorted by: {kw})."


def update_extensions_impl(w, state):
    fname = w["file_sel"].value
    if not fname:
        w["ext_sel"].options = []
        return

    if fname not in state["ext_cache"]:
        state["ext_cache"][fname] = scan_image_extensions(fname)

    exts = state["ext_cache"][fname]
    w["ext_sel"].options = exts

    if exts:
        w["ext_sel"].value = exts[0]

    # Populate header extension list
    try:
        import astropy.io.fits as fits
        with fits.open(fname, memmap=False) as hdul:
            ext_names = [
                h.name if h.name else f"EXT{i}"
                for i, h in enumerate(hdul)
            ]
    except Exception:
        ext_names = ["PRIMARY"]

    # Update dropdown widget used for header display
    w["hdr_ext"].options = ext_names
    w["hdr_ext"].value = ext_names[0]


def update_sourcelets_impl(w, instr):
    fname = w["file_sel"].value
    ename = w["ext_sel"].value

    if not fname or not ename:
        w["src_sel"].visible = False
        return

    try:
        import astropy.io.fits as fits
        with fits.open(fname, memmap=False) as hdul:
            for h in hdul:
                if (
                    h.name == ename
                    and isinstance(h.data, np.ndarray)
                    and h.data.ndim == 3
                ):
                    ns = h.data.shape[0]
                    names = instr["sourcelets"]
                    opts = [names.get(i, f"src{i}") for i in range(ns)]
                    w["src_sel"].options = opts
                    w["src_sel"].value = opts[0]
                    w["src_sel"].visible = True
                    return

    except Exception:
        pass

    w["src_sel"].visible = False


def current_arr(w, instr, state):
    """Return arithmetic array if active, else base array."""
    fname = w["file_sel"].value
    ename = w["ext_sel"].value

    if not fname or ename is None:
        return None

    src_idx = None
    if w["src_sel"].visible:
        lbl = w["src_sel"].value
        names = instr["sourcelets"]
        src_idx = next((i for i, n in names.items() if n == lbl), 0)

    if state["arith_active"] and state["arith_arr"] is not None:
        return state["arith_arr"]

    return load_image_slice(fname, ename, src_idx)


def update_idx_impl(w):
    idx = w["file_idx"].value - 1
    files = list(w["file_sel"].options.values())
    if 0 <= idx < len(files):
        w["file_sel"].value = files[idx]


def autofetch_tick_impl(w, instr):
    """
    Periodically scans the folder and updates to the latest file.
    Runs only while autofetch is enabled.
    """
    folder = w["input_dir"].value
    ftype = w["filetype"].value
    path = Path(folder).expanduser()

    files = find_instrument_files(path, ftype, instr)
    if not files:
        return

    # Sort like scan_folder does, using the predefined keyword
    kw = w["sort_key"].value.strip()

    def sort_key(f):
        v = safe_get_header_value(f, kw)
        try:
            return float(v)
        except Exception:
            return str(v) if v is not None else ""

    files = sorted(map(str, map(Path.resolve, files)), key=sort_key)
    last = files[-1]

    if last != w["file_sel"].value:
        w["file_sel"].options = {Path(f).name: f for f in files}
        w["file_sel"].value = last