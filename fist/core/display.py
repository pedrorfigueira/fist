# image setup and display tools

import numpy as np
from bokeh.plotting import figure
from bokeh.models import DataRange1d, ColumnDataSource
from bokeh.events import Reset
import matplotlib.cm as cm

def rgba_uint32_from_norm(arr01, cmap_name="viridis"):
    cmap = cm.get_cmap(cmap_name)
    rgba = cmap(arr01, bytes=True)  # (h,w,4)

    r = rgba[...,0].astype(np.uint32)
    g = rgba[...,1].astype(np.uint32)
    b = rgba[...,2].astype(np.uint32)
    a = rgba[...,3].astype(np.uint32)

    # Bokeh expects: 0xAABBGGRR (little-endian)
    return (a << 24) | (b << 16) | (g << 8) | r

def make_image_figure():
    fig = figure(
        toolbar_location="right",
        tools="pan,wheel_zoom,box_zoom,reset,save",
        x_range=(0, 1),
        y_range=(0, 1),
        match_aspect=False,    # important: allow non-square pixels
    )

    # let Panel manage sizing and allow figure to grow to available space in containers.
    fig.height_policy = "max"
    fig.width_policy  = "max"

    return fig

def set_image(fig, arr01, cmap):
    arr01 = np.nan_to_num(arr01, nan=0.0)
    arr01 = np.clip(arr01, 0, 1)

    h, w = arr01.shape
    rgba = rgba_uint32_from_norm(arr01, cmap)

    # STEP 1: read previous image shape (stored on figure)
    prev_shape = getattr(fig, "_image_shape", None)

    # Find existing image renderer
    renderer = None
    for r in fig.renderers:
        if hasattr(r, "glyph") and r.glyph.__class__.__name__ == "ImageRGBA":
            renderer = r
            break

    # STEP 2: if shape changed, remove renderer
    if renderer is not None and prev_shape != (h, w):
        fig.renderers.remove(renderer)
        renderer = None

    # STEP 3: create or update renderer
    if renderer is None:
        fig.image_rgba(image=[rgba], x=0, y=0, dw=w, dh=h)
    else:
        renderer.data_source.data = dict(
            image=[rgba], x=[0], y=[0], dw=[w], dh=[h]
        )

    # STEP 4: update ranges
    fig.x_range.start = 0
    fig.x_range.end   = w
    fig.y_range.start = 0
    fig.y_range.end   = h

    # STEP 5: store shape for next call
    fig._image_shape = (h, w)



