# main entry for fist panel app

from pathlib import Path
import numpy as np

import panel as pn


from bokeh.models import ColumnDataSource

from fist.core.state import _state
from fist.core.loader import  load_image_slice
from fist.core.instruments import load_instrument
from fist.core.sessionmng import (
    scan_folder_impl, update_extensions_impl, update_sourcelets_impl, update_idx_impl,
    autofetch_tick_impl, current_arr
)
from fist.core.scaling import percentile_clip
from fist.core.transforms import apply_transform
from fist.core.display import make_image_figure, set_image
from fist.core.layout import build_widgets, assemble_layout
from fist.tools.arithmetic import compute_arithmetic
from fist.tools.analysis import update_cut_plot, compute_region_stats
from fist.tools.header import update_header_impl, apply_header_filter_impl


def build_app(instrument_name, start_folder):

    pn.extension()
    
    # -------------------------------
    # Initialization
    # -------------------------------
    
    # load instrument config
    instr = load_instrument(instrument_name)
    # copying instrument image transform starting state
    _state["transform"] = instr["transform"].copy()
    
    # If CLI folder not provided → use the instrument's default
    if start_folder is None:
        start_folder = instr.get("start_folder", ".")
    else:
        # Always store user-defined folder back into instrument config
        instr["start_folder"] = start_folder

    w = build_widgets(instr)

    image_fig = make_image_figure()

    image_pane = pn.pane.Bokeh(image_fig, sizing_mode="stretch_both")

    cut_src = w["cut_src"]

    layout = assemble_layout(w, image_pane, instr)

    # Source for region outline (circle or square)
    w["region_src"] = ColumnDataSource(data=dict(xs=[], ys=[]))

    # -------------------------------
    # Autofetch
    # -------------------------------

    # Periodic callback handle
    autofetch_cb = None

    def autofetch_tick():
        autofetch_tick_impl(w, instr)
        update_extensions()
        update_image()

    # -------------------------------
    # Core update logic
    # -------------------------------

    def update_extensions(event=None):
        update_extensions_impl(w, _state)
        update_sourcelets()


    def update_sourcelets(event=None):
        update_sourcelets_impl(w, instr)

    def apply_header_filter(event=None):
        apply_header_filter_impl(w)

    def update_header(event=None):
        update_header_impl(w)


    # -------------------------------
    # Folder scanning
    # -------------------------------

    def scan_folder(event=None):
        scan_folder_impl(w, instr, _state)
        update_extensions()
        update_image()


    def update_idx(event=None):
        update_idx_impl(w)
        update_image()


    def update_slider_from_dropdown(event=None):
        try:
            file_values = list(w["file_sel"].options.values())
            idx = file_values.index(w["file_sel"].value)
            w["file_idx"].value = idx + 1
        except Exception:
            pass


    # -------------------------------
    # handler functions
    # -------------------------------
        
    def on_autofetch_toggle(event):
        nonlocal autofetch_cb

        if w["autofetch"].value:
            # Turn ON autofetch
            w["autofetch"].name = "Stop Autofetch"

            # Start periodic callback every 2 seconds (adjust as needed)
            autofetch_cb = pn.state.add_periodic_callback(
                autofetch_tick,
                period=2000,   # ms
                timeout=None
            )
        else:
            # Turn OFF autofetch
            w["autofetch"].name = "Enable Autofetch"

            if autofetch_cb is not None:
                autofetch_cb.stop()
                autofetch_cb = None

    def toggle_section(toggle_widget, section_widget):
        """General show/hide handler for collapsible sections."""
        if toggle_widget.value:
            toggle_widget.name = "Hide"
            section_widget.visible = True
        else:
            toggle_widget.name = "Show"
            section_widget.visible = False


    # -------------------------------
    # Main image update
    # -------------------------------

    def update_cut_overlay():
        if not w["cuts_on"].value or not w["cuts_toggle"].value:
            # Hide overlay when cuts are disabled or panel collapsed
            w["cut_overlay_src"].data = dict(x=[], y=[])
            w["cut_points_src"].data = dict(x=[], y=[])
            return

        try:
            x1 = float(w["x1"].value)
            y1 = float(w["y1"].value)
            x2 = float(w["x2"].value)
            y2 = float(w["y2"].value)
        except:
            return

        # Update line (two points)
        w["cut_overlay_src"].data = dict(
            x=[x1, x2],
            y=[y1, y2],
        )

        # Update endpoints (two circle markers)
        w["cut_points_src"].data = dict(
            x=[x1, x2],
            y=[y1, y2],
        )


    def update_region_overlay():
        """
        Draw region outline and compute statistics for the selected region.
        Updates the cyan multi_line glyph AND the Markdown statistics box.
        """
        # If toggle is off → clear overlay + stats
        if not w["region_toggle"].value or not w["region_on"].value:
            w["region_src"].data = dict(xs=[], ys=[])
            return

        shape = w["region_shape"].value   # Circle | Square
        x = float(w["region_x"].value)
        y = float(w["region_y"].value)
        d = float(w["region_d"].value)

        arr = current_arr(w, instr, _state)
        if arr is None:
            w["region_stats"].object = "No array loaded."
            return

        h, wimg = arr.shape  # height, width

        # ---------------------------------
        # 1) Build outline for display
        # ---------------------------------
        if shape == "Circle":
            theta = np.linspace(0, 2*np.pi, 100)
            xs = (x + d * np.cos(theta)).tolist()
            ys = (y + d * np.sin(theta)).tolist()
            xs.append(xs[0]); ys.append(ys[0])
            w["region_src"].data = dict(xs=[xs], ys=[ys])

        else:  # Square
            xs = [x, x+d, x+d, x, x]
            ys = [y, y,   y+d, y+d, y]
            w["region_src"].data = dict(xs=[xs], ys=[ys])

        # ---------------------------------
        # 2) Build mask for statistics
        # ---------------------------------
        yy, xx = np.indices(arr.shape)

        if shape == "Circle":
            mask = (xx - x)**2 + (yy - y)**2 <= d**2

        else:  # Square
            mask = (xx >= x) & (xx <= x+d) & (yy >= y) & (yy <= y+d)

        # Avoid invalid indices if user inputs go outside image
        mask = mask & (xx >= 0) & (xx < wimg) & (yy >= 0) & (yy < h)

        # ---------------------------------
        # 3) Compute statistics
        # ---------------------------------
        stats_text = compute_region_stats(arr, mask)
        w["region_stats"].object = stats_text


    def update_image(event=None):
        fname = w["file_sel"].value
        ename = w["ext_sel"].value

        # allows PRIMARY or unnamed extensions
        if not fname or ename is None:
            return

        src_idx=None
        if w["src_sel"].visible:
            lbl = w["src_sel"].value
            sourcelet_names = instr["sourcelets"]
            src_idx = next((i for i,nm in sourcelet_names.items() if nm==lbl), 0)

        arr_base = load_image_slice(fname, ename, src_idx)
        if arr_base is None:
            w["info_file"].object = "Cannot load image."
            return

        # ---- Arithmetic ----
        if w["arith_on"].value and w["arith_file"].value != "None":
            arr2 = load_image_slice(w["arith_file"].value, ename, src_idx)
            if arr2 is None:
                w["info_file"].object="Arithmetic error"
                return
            arr, nan_warn = compute_arithmetic(arr_base, arr2, w["arith_op"].value)
            _state["arith_active"] = True
            _state["arith_arr"] = arr
            _state["arith_nan_warning"] = nan_warn
        else:
            arr = arr_base
            _state["arith_active"] = False
            _state["arith_arr"] = None
            _state["arith_nan_warning"] = False

        # ---- Scaling ----
        arr_s = percentile_clip(
            arr,
            w["vmin"].value, w["vmax"].value,
            w["gamma"].value,
            stretch=w["stretch"].value,
            contrast=w["contrast"].value
        )

        # ---- Transform ----
        arr_s = apply_transform(arr_s, _state["transform"])

        # ---- Display ----
        set_image(image_fig, arr_s, w["cmap"].value)
        
        w["info_file"].object = f"Read {Path(fname).name} ({arr_s.shape[1]} x {arr_s.shape[0]})."

        # ---- Cuts ----
        if w["cuts_toggle"].value:

            # Add glyphs once
            if not getattr(image_fig, "_cuts_added", False):
                image_fig.line(
                    x="x", y="y",
                    source=w["cut_overlay_src"],
                    line_color="yellow", line_width=3
                )
                image_fig.scatter(
                    x="x", y="y",
                    source=w["cut_points_src"],
                    marker="circle", size=10, color="yellow"
                )
                image_fig._cuts_added = True

            # Update plot and overlay
            update_cut_plot(
                arr,
                float(w["x1"].value), float(w["y1"].value),
                float(w["x2"].value), float(w["y2"].value),
                cut_src,
            )
            update_cut_overlay()

        else:
            # toggle = OFF → clear overlays
            w["cut_overlay_src"].data = dict(x=[], y=[])
            w["cut_points_src"].data = dict(x=[], y=[])

        # ---- Region ----
        if w["region_toggle"].value:
            # add multi_line glyph once
            if not getattr(image_fig, "_region_added", False):
                image_fig.multi_line(
                    xs="xs", ys="ys",
                    source=w["region_src"],
                    line_color="cyan", line_width=2
                )
                image_fig._region_added = True

            # update overlay (function ensures proper show/clear)
            update_region_overlay()
        else:
            # panel hidden -> ensure overlay cleared
            w["region_src"].data = dict(xs=[], ys=[])

        # ---- Header ----
        if w["hdr_toggle"].value:
            update_header()


    # -------------------------------
    # Wire events / Watchers
    # -------------------------------

    w["refresh"].on_click(scan_folder)
    w["file_idx"].param.watch(update_idx, "value")
    w["file_sel"].param.watch(update_slider_from_dropdown, "value")

    w["file_sel"].param.watch(update_extensions, "value")
    w["ext_sel"].param.watch(lambda e: (update_sourcelets(), update_image()), "value")
    w["src_sel"].param.watch(update_image, "value")

    w["sort_key"].param.watch(scan_folder, "value")
    w["autofetch"].param.watch(on_autofetch_toggle, "value")

    # key=key to freeze the value inside the lambda 
    for key in ('disp', 'trans', 'arith', 'cuts', 'region', 'hdr'):
        w[f"{key}_toggle"].param.watch(
            lambda evt, key=key: toggle_section(w[f"{key}_toggle"], w[f"{key}_section"]),
            "value"
        )
        
    # display

    for key in ("vmin","vmax","gamma","contrast","stretch","cmap"):
        w[key].param.watch(update_image, "value")

    # transforms

    w["flip_x"].param.watch(lambda e: (_state["transform"].__setitem__("flip_x", w["flip_x"].value), update_image()), "value")
    w["flip_y"].param.watch(lambda e: (_state["transform"].__setitem__("flip_y", w["flip_y"].value), update_image()), "value")
    w["neg"].param.watch(lambda e: (_state["transform"].__setitem__("negative", w["neg"].value), update_image()), "value")
    
    def on_rotate_click(event):
        _state["transform"]["rot90"] = (_state["transform"]["rot90"] + 1) % 4
        update_image()

    w["rot90"].on_click(on_rotate_click)

    # Arithmetic

    for key in ("arith_on", "arith_op", "arith_file"):
        w[key].param.watch(update_image, "value")

    # Cuts

    w["cuts_on"].param.watch(update_image, "value")
    w["cuts_on"].param.watch(lambda e: update_cut_overlay(), "value")
    w["cuts_toggle"].param.watch(lambda e: update_cut_overlay(), "value")

    for key in ("x1","y1","x2","y2"):
        w[key].param.watch(lambda e: update_cut_overlay(), "value")
        w[key].param.watch(update_image, "value")

    # Region 

    w["region_on"].param.watch(update_image, "value")
    w["region_on"].param.watch(lambda e: update_region_overlay(), "value")
    w["region_toggle"].param.watch(lambda e: update_region_overlay(), "value")

    for key in ("region_shape", "region_x", "region_y", "region_d"):
        w[key].param.watch(lambda e: update_region_overlay(), "value")
        w[key].param.watch(update_image, "value")
        
    # Header

    w["hdr_ext"].param.watch(update_header, "value")
    w["file_sel"].param.watch(lambda e: (update_extensions(), update_header()), "value")
    w["hdr_search"].param.watch(apply_header_filter, "value")
    w["hdr_toggle"].param.watch(lambda e: update_header(), "value")

    # Initial load
    scan_folder()

    return layout


