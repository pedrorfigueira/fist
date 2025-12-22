# header handling tools

def apply_header_filter_impl(w):
    full_text = w["hdr_full_text"]
    query = w["hdr_search"].value.strip().lower()

    if not query:
        filtered = full_text
    else:
        lines = [
            line for line in full_text.split("\n")
            if query in line.lower()
        ]
        filtered = "\n".join(lines) if lines else "No matches found."

    w["hdr_pane"].object = (
        "<pre style='white-space: pre; font-family: monospace;'>"
        + filtered +
        "</pre>"
    )


def update_header_impl(w):
    fname = w["file_sel"].value
    ext = w["hdr_ext"].value

    if not fname or ext is None:
        return

    import astropy.io.fits as fits
    try:
        with fits.open(fname) as hdul:
            hdr = hdul[ext].header
    except Exception as e:
        w["hdr_pane"].object = f"<pre>Error loading header: {e}</pre>"
        return

    # build text exactly like FITS header formatting
    lines = [f"{k:<20} = {v}" for k, v in hdr.items()]
    text = "\n".join(lines) + "\n\n"

    # store raw text for later searching
    w["hdr_full_text"] = text

    w["hdr_pane"].object = (
        "<pre style='white-space: pre; font-family: monospace;'>"
        + text +
        "</pre>"
    )

    apply_header_filter_impl(w)