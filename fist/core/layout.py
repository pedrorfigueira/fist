# layout and widget definitions for the web interface

import panel as pn

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

from importlib.resources import files

def make_cut_figure():
    src = ColumnDataSource(data=dict(x=[], y=[]))
    fig = figure(height=300, width=600,
                 tools="pan,wheel_zoom,box_zoom,reset",
                 title="Diagonal Cut")
    fig.line("x", "y", source=src, line_width=2, color="orange")
    return fig, src

def build_widgets(instr):
    """Create a dict of all widgets."""
    
    w = {}
    
    w["refresh"]   = pn.widgets.Button(name="Scan Input Folder", button_type="primary", width=120)
    w["autofetch"] = pn.widgets.Toggle(name="Enable Autofetch", value=instr["autofetch"], button_type="primary", width=120)

    w["input_dir"] = pn.widgets.TextInput(name="Input folder", value=instr["start_folder"], width=345)
    w["filetype"]  = pn.widgets.Select(name="File type", value=instr["default_filetype"],
                                       options=instr["filetype_list"], width=210)

    w["file_sel"]  = pn.widgets.Select(name="File", options=[], width=400)
    w["file_idx"]  = pn.widgets.IntSlider(name="Index", start=1, end=1, value=1, step=1, width=345)
    w['sort_key'] =  pn.widgets.TextInput(name="Sort Key", value=instr["sort_key"], width=210)

    w["ext_sel"]   = pn.widgets.Select(name="Extension", options=[], width=250)
    w["src_sel"]   = pn.widgets.Select(name="Sourcelet", options=[], width=250)

    w["info_state"] = pn.pane.Markdown("Ready.", width=200)
    w["info_file"] = pn.pane.Markdown("", width=350)

    # Display controls
    
    w["disp_toggle"] = pn.widgets.Toggle(name="Show", value=False,        
        button_type="success", width=80)
        
    scale = instr["default_scaling"]
    
    w["vmin"]      = pn.widgets.FloatSlider(name="vmin %", start=0,end=50,value=scale["vmin"], width=275)
    w["vmax"]      = pn.widgets.FloatSlider(name="vmax %", start=50,end=100,value=scale["vmax"], width=275)
    w["gamma"]     = pn.widgets.FloatSlider(name="Gamma", start=0.1,end=3,value=scale["gamma"], width=275)
    w["contrast"]  = pn.widgets.FloatSlider(name="Contrast",
                                            start=0.1, end=3, value=scale["contrast"], width=275)
    w["stretch"]   = pn.widgets.Select(name="Stretch",
                        options=["linear","log","sqrt","arcsinh","zscale"], value=scale["stretch"], width=275)
    w["cmap"]      = pn.widgets.Select(name="Colormap",
                                       options=["viridis","gray","plasma","magma",
                                                "inferno","cividis","hot"],
                                       value=instr["default_cmap"], width=275)
    w["disp_section"] = pn.Column(
        pn.Row(pn.Spacer(width=20), w["vmin"], w["vmax"]),
        pn.Row(pn.Spacer(width=20), w["gamma"], w["contrast"]),
        pn.Row(pn.Spacer(width=20), w["stretch"], w["cmap"]),
        visible=False       
    )

    # transforms
    
    w["trans_toggle"] = pn.widgets.Toggle(name="Show", value=False,
        button_type="success", width=80)
    
    w["flip_x"] = pn.widgets.Toggle(name="↔ flip_x", value=instr["transform"]["flip_x"])
    w["flip_y"] = pn.widgets.Toggle(name="↕ flip_y", value=instr["transform"]["flip_y"])
    w["rot90"]  = pn.widgets.Button(name="⟳90°")
    w["neg"]    = pn.widgets.Toggle(name="⊖ negative", value=instr["transform"]["neg"])
    
    w["trans_section"] = pn.Row(
        pn.Spacer(width=150), w["flip_x"], w["flip_y"], w["rot90"], w["neg"],
        visible=False     
    )

    # arithmetic
    
    w["arith_toggle"] = pn.widgets.Toggle(name="Show", value=False,
        button_type="success", width=80)
    
    w["arith_on"] = pn.widgets.Toggle(name="Compute", value=False)
    w["arith_op"] = pn.widgets.Select(name="Op", options=["-","+","/","x"], width=50)
    w["arith_file"] = pn.widgets.Select(name="Second file", options=["None"], width=385)
    
    w["arith_section"] = pn.Column(
        pn.Row(pn.Spacer(width=20), w["arith_on"], pn.Spacer(width=7), w["arith_op"], pn.Spacer(width=7), w["arith_file"]),
        visible=False  
    )

    # cuts
    
    w["cuts_toggle"] = pn.widgets.Toggle(name="Show", value=False,
        button_type="success", width=80)
    
    w["cuts_on"] = pn.widgets.Toggle(name="Show cuts", value=False)
    w["x1"] = pn.widgets.FloatInput(name="x1", width=80, value=0)
    w["y1"] = pn.widgets.FloatInput(name="y1", width=80, value=0)
    w["x2"] = pn.widgets.FloatInput(name="x2", width=80, value=10)
    w["y2"] = pn.widgets.FloatInput(name="y2", width=80, value=10)
    
    fig, src = make_cut_figure()
    w["cut_fig"] = fig
    w["cut_src"] = src
    w["cut_panel"] = pn.pane.Bokeh(fig, visible=False)
    
    
    w["cut_overlay_src"] = ColumnDataSource(data=dict(x=[], y=[]))
    w["cut_points_src"] = ColumnDataSource(data=dict(x=[], y=[]))

    w["cuts_section"] = pn.Column(
        pn.Row(pn.Spacer(width=45), w["cuts_on"], pn.Spacer(width=25), w["x1"], w["y1"], w["x2"], w["y2"]),
        pn.Row(pn.Spacer(width=20), w["cut_panel"]),
        visible=False  
    )

    # region 

    w["region_toggle"] = pn.widgets.Toggle(name="Show", value=False,
        button_type="success", width=80)

    w["region_on"] = pn.widgets.Toggle(name="Draw & Compute", value=False)       
    w["region_shape"] = pn.widgets.Select(name="Shape", options=["Circle", "Square"], 
        width=80, value="Circle")

    w["region_x"] = pn.widgets.FloatInput(name="x", width=80, value=10.0)
    w["region_y"] = pn.widgets.FloatInput(name="y", width=80, value=10.0)
    w["region_d"] = pn.widgets.FloatInput(name="d", width=80, value=5.0)

    w["region_stats"] = pn.pane.Markdown("", width=620)

    w["region_section"] = pn.Column(
        pn.Row(pn.Spacer(width=35), w["region_on"], pn.Spacer(width=20), w["region_shape"], w["region_x"], w["region_y"], w["region_d"]),
        pn.Row(pn.Spacer(width=10), w["region_stats"]),
        visible=False
    )

    # header
    w["hdr_toggle"] = pn.widgets.Toggle(name="Show", value=False,
        button_type="success", width=80)
    
    w["hdr_ext"] = pn.widgets.Select(name="Header Extension", options=["PRIMARY"], value="PRIMARY", width=160)
    w["hdr_search"] = pn.widgets.TextInput(name="Search", placeholder="Type to filter header...", width=300)
    w["hdr_full_text"] = ""     # stores full header text (unfiltered)
    w["hdr_pane"] = pn.pane.HTML("<pre></pre>", width=700, height=300)
    
    w["hdr_section"] = pn.Column(
        pn.Row(pn.Spacer(width=20), w["hdr_ext"], pn.Spacer(width=20), w["hdr_search"]),
        pn.Row(pn.Spacer(width=10), w["hdr_pane"]),
        visible=False  
    )

    return w
    
def assemble_layout(widgets, image_pane, instr):

    logo_path = files("fist.static") / "FISTlogo.png"
    logo_pane = pn.pane.PNG(str(logo_path), width=85) 
    
    instr_name = instr["name"]
    
    left = pn.Column(
        pn.Spacer(height=5),
        pn.Row(pn.Spacer(width=20),
        logo_pane, pn.Spacer(width=20), 
        pn.Column(pn.pane.HTML("<h2> FITS Inspection Streamlined Tool</h2>"), pn.pane.Markdown(f"### handling *{instr_name}*"), pn.pane.Markdown(width=10)),
        pn.Column(pn.Spacer(height=10), widgets["refresh"], widgets["autofetch"])),
        pn.Row(pn.Spacer(width=20), widgets["input_dir"], widgets["filetype"]),
        pn.Row(pn.Spacer(width=20), widgets["file_idx"], widgets["sort_key"]),
        pn.Row(pn.Spacer(width=40), widgets["file_sel"]),
        pn.Row(pn.Spacer(width=30), widgets["ext_sel"], widgets["src_sel"]),
        pn.Row(pn.Spacer(width=15), widgets["info_state"], pn.Spacer(width=7), widgets["info_file"]),
        pn.Row(pn.Spacer(width=10), pn.pane.Markdown("---", width=590, height=10)),
        pn.Row(pn.Spacer(width=85), pn.pane.Markdown("### Display"), pn.Spacer(width=10), widgets["disp_toggle"], 
            pn.Spacer(width=75), pn.pane.Markdown("### Transforms"), pn.Spacer(width=10), widgets["trans_toggle"]),
        widgets["disp_section"], 
        widgets["trans_section"],
        pn.Row(pn.Spacer(width=10), pn.pane.Markdown("---", width=590, height=10)),
        pn.Row(pn.Spacer(width=195), pn.pane.Markdown("### Image Arithmetic"), pn.Spacer(width=10), widgets["arith_toggle"]),
        widgets["arith_section"],
        pn.Row(pn.Spacer(width=10), pn.pane.Markdown("---", width=590, height=10)),
        pn.Row(pn.Spacer(width=40), pn.pane.Markdown("### Cuts"), pn.Spacer(width=10), widgets["cuts_toggle"],
            pn.Spacer(width=15), pn.pane.Markdown("### Region"), pn.Spacer(width=10), widgets["region_toggle"],
            pn.Spacer(width=15), pn.pane.Markdown("### Header"), pn.Spacer(width=10), widgets["hdr_toggle"]),
        widgets["cuts_section"],
        widgets["region_section"],
        widgets["hdr_section"],
        width=630,
        height_policy="auto",
    )

    right = pn.Column(
        image_pane,
        sizing_mode="stretch_both",
        height_policy="max",
        width_policy="max"
    )

    return pn.Row(left, right, sizing_mode="stretch_both", height_policy="auto", width_policy="auto")

