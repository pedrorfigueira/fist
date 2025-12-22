"""
Central registry for instrument-specific configuration.

Allows the viewer to support multiple instruments
simply by selecting a configuration block.
"""

# -----------------------------
# Generic instrument definition
# -----------------------------

DEFAULT_CONFIG = dict(
    name = "Generic Instrument",
    
    # folder where to search for FITS images
    start_folder = ".",
    
    # Automatically fetch most recent file of default filetype
    autofetch = False,
    
    # Key for sorting files
    sort_key = "MJD-OBS",
    
    # display values
    default_scaling = {
        "vmin": 1.0,
        "vmax": 99.0,
        "gamma": 1.0,
        "contrast": 1.0,
        "stretch": "linear",
    },
    
    # transform starting state
    transform = {
        "flip_x": False, 
        "flip_y": False, 
        "rot90": 0, 
        "neg": False,
    },

    # colormap
    default_cmap = "viridis",

)

# -------------------------
# KPF instrument properties
# -------------------------

KPF_CONFIG = DEFAULT_CONFIG.copy()

KPF_CONFIG.update(
    # Human-readable name
    name = "Keck Planet Finder (KPF)",

    start_folder = "spectra/",

    # Sourcelet mapping (what SOURCELET_NAMES currently defines)
    sourcelets = {
        0: "orderlet1",
        1: "orderlet2",
        2: "orderlet3",
        3: "CAL",
        4: "SKY",
    },
    
    filetypes = {
        "2D": "*_2D.fits",
        "L1": "*_L1.fits",
        "L2": "*_L2.fits",
    },

    # filetypes for listing
    filetype_list = ["2D", "L1", "L2"],

    # filetype chose at runtime
    default_filetype = "L2",

)


# ------------------------------
# ESPRESSO instrument properties
# ------------------------------

ESPRESSO_CONFIG = DEFAULT_CONFIG.copy()

ESPRESSO_CONFIG.update(
    name="ESPRESSO",

    filetypes={
        "guiding": "G-ESPRE.*.fits",
        "CCF_A": "r.ESPRE.*_CCF_A.fits",
        "CCF_TCOR_A": "r.ESPRE.*_CCF_TELL_CORR_A.fits",
        "S2D_A": "r.ESPRE.*_S2D_A.fits",
        "S2D_B": "r.ESPRE.*_S2D_B.fits",
        "S2D_BLZ_A": "r.ESPRE.*_S2D_BLAZE_A.fits",
        "S2D_BLZ_B": "r.ESPRE.*_S2D_BLAZE_B.fits",
        "S2D_BLZ_TCOR_A": "r.ESPRE.*_S2D_BLAZE_TELL_CORR_A.fits",
        "S2D_TCOR_A": "r.ESPRE.*_S2D_TELL_CORR_A.fits",
        "S2D_TELL_SPEC_A": "r.ESPRE.*_S2D_TELL_SPECTRUM_A.fits",
    },

    # filetypes for listing
    filetype_list=["guiding", "CCF_A", "CCF_TCOR_A", "S2D_A", "S2D_B",
                   "S2D_BLZ_A", "S2D_BLZ_B", "S2D_BLZ_TCOR_A", "S2D_TCOR_A", "S2D_TELL_SPEC_A"],

    # filetype chose at runtime
    default_filetype="CCF_A",
)

# ------------------------------
# CORALIE instrument properties
# ------------------------------

CORALIE_CONFIG = DEFAULT_CONFIG.copy()

CORALIE_CONFIG.update(
    name="CORALIE",

    filetypes={
        "guiding": "GCORALIE.*.fits",
        "CCF_A": "CORALIE.*_ccf_*_A.fits",
        "BIS_A": "CORALIE.*_bis_*_A.fits",
        "E2DS_A": "CORALIE.*_e2ds_A.fits",
        "E2DS_B": "CORALIE.*_e2ds_B.fits",
        "BLAZE_A": "CORALIE.*_blaze_A.fits",
        "BLAZE_B": "CORALIE.*_blaze_B.fits",
    },

    # filetypes for listing
    filetype_list=["guiding", "CCF_A", "BIS_A", "E2DS_A", "E2DS_B", "BLAZE_A", "BLAZE_B"],

    # filetype chose at runtime
    default_filetype="CCF_A",
)

# ------------------------------
# HARPS instrument properties
# ------------------------------

HARPS_CONFIG = DEFAULT_CONFIG.copy()

HARPS_CONFIG.update(
    name="HARPS",

    filetypes={
        "CCF_A": "r.HARPS.*_CCF_A.fits",
        "S2D_A": "r.HARPS.*_S2D_A.fits",
        "S2D_B": "r.HARPS.*_S2D_B.fits",
        "S2D_BLAZE_A": "r.HARPS.*_S2D_BLAZE_A.fits",
        "S2D_BLAZE_B": "r.HARPS.*_S2D_BLAZE_B.fits",
    },

    # filetypes for listing
    filetype_list=["CCF_A", "S2D_A", "S2D_B", "S2D_BLAZE_A", "S2D_BLAZE_B"],

    # filetype chose at runtime
    default_filetype="CCF_A",
)

# ------------------------------
# HARPS-N instrument properties
# ------------------------------

HARPN_CONFIG = HARPS_CONFIG.copy()

HARPN_CONFIG.update(
    name="HARPS-N",

    filetypes={
        "CCF_A": "r.HARPN.*_CCF_A.fits",
        "S2D_A": "r.HARPN.*_S2D_A.fits",
        "S2D_B": "r.HARPN.*_S2D_B.fits",
        "S2D_BLAZE_A": "r.HARPN.*_S2D_BLAZE_A.fits",
        "S2D_BLAZE_B": "r.HARPN.*_S2D_BLAZE_B.fits",
    },
)

# -----------------------
# Registry of instruments
# -----------------------

INSTRUMENTS = {
    "KPF": KPF_CONFIG,
    "ESPRESSO": ESPRESSO_CONFIG,
    "CORALIE": CORALIE_CONFIG,
    "HARPS": HARPS_CONFIG,
    "HARPS-N": HARPN_CONFIG,
}

# -------------------------
# Loader helper
# -------------------------

def load_instrument(name="KPF"):
    """
    Return a deep copy of the configuration for a given instrument.
    """
    import copy
    try:
        return copy.deepcopy(INSTRUMENTS[name])
    except KeyError:
        raise ValueError(f"Unknown instrument: {name}. "
                         f"Available: {list(INSTRUMENTS.keys())}")

