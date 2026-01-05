#!/usr/bin/env python3

import sys
import argparse
import panel as pn

from importlib.resources import files, as_file

from fist.app import build_app


def main():
    parser = argparse.ArgumentParser(
        description="FITS Inspection Streamlined Tool",
        epilog=(
            "Examples:\n"
            "  fist --instrument ESPRESSO --folder example (to run the example)\n"
            "  fist --instrument KPF --folder /path/to/fits\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--instrument", type=str, default="KPF",
                        help="Instrument name (e.g. KPF)")
    parser.add_argument("--folder", type=str, default=None,
                        help="Folder to load FITS files from")
    parser.add_argument("--port", type=int, default=5006,
                    help="Port for the Panel server (default: 5006)")
    parser.add_argument("--show", action="store_true", default=True,
                    help="Open the application in a browser at startup.")

    args = parser.parse_args()

    ins_name = args.instrument.upper()

    # example folder definition
    if args.folder is not None:
        if args.folder.upper() == "EXAMPLE":
            with as_file(files("fist.static")) as p:
                args.folder = str(p)
    
    # ------------------------------------------------------------------
    # Startup printout
    # ------------------------------------------------------------------
    print(
        f"\n🔭  Launching FIST! \n"
        f"    Instrument : {ins_name}\n"
        f"    Folder     : {args.folder}\n"
        f"    Port       : {args.port}\n"
    )

    # ------------------------------------------------------------------
    # Build Panel application
    # ------------------------------------------------------------------

    # Build Panel layout dynamically
    app = build_app(instrument_name=ins_name, start_folder=args.folder)

    # Start the Panel server
    pn.serve(
        {f"FIST-{ins_name}": app},
        show=args.show,
        autoreload=False,
        port=args.port,
        title="FIST"
    )

if __name__ == "__main__":
    main()

