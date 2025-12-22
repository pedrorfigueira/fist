---
title: "FIST: a lightweight interactive tool for rapid inspection and analysis of astronomical FITS images"
tags:
  - astronomy
  - FITS
authors:
  - name: Pedro Figueira
    orcid: 0000-0001-8504-283X
    affiliation: 1
affiliations:
  - name: Instituto de Astrofísica de Andalucía-CSIC, Glorieta de la Astronomía s/n, E-18008 Granada, Spain
    index: 1
date: 2025-12-22
bibliography: paper.bib
---

## Summary

Astronomical data products are commonly stored in the Flexible Image Transport System (FITS) format, often as multi-extension images or three-dimensional data cubes. Several mature viewers exist for FITS data, such as DS9 [@DS9] and ESO’s Real-Time Display (RTD) [@RTD]. While these tools provide powerful image visualization capabilities, they offer limited support for scripting and automation.

**FIST** (FITS Inspection Streamlined Tool) is a Python-based interactive visualization application designed to enable rapid visual inspection, interactive manipulation, and instrument-specific quick-look analysis, particularly in observatory and pipeline-development contexts. It provides a browser-based interface for exploring FITS images using standard image transformations, image arithmetic operations, and interactive analysis tools such as cuts and region statistics. FIST supports multi-extension FITS files, three-dimensional data cubes, and instrument-specific configurations, enabling efficient inspection of heterogeneous data products without requiring custom scripts or heavyweight frameworks.

FIST is implemented using the scientific Python ecosystem, notably NumPy, Astropy, Bokeh, Panel and Matplotlib, and is distributed as an installable Python package with a command-line entry point. It is intended both as a ready-to-use inspection tool and as a starting point for the development of custom quick-look or pipeline-monitoring applications. It can easily be adapted to common tasks such as calibration comparison, sky conditions assessment, or spectral line inspection.

---

## Statement of Need

Modern astronomical instruments and pipelines routinely generate large volumes of FITS data with complex internal structures, including multiple extensions, auxiliary image products, and three-dimensional arrays. During observations, instrument commissioning, and pipeline development, scientists often require fast, interactive feedback on data quality, structure, and basic statistics, without the overhead of writing custom visualization code or deploying large analysis environments.

Existing FITS viewers and analysis tools provide powerful capabilities, but they are typically geared toward stand-alone usage or rely on dedicated scripting syntaxes. This does not fully address the needs of many astronomers, who could benefit from tools that:

- can be launched quickly on local or remote systems,
- support instrument-specific conventions and file patterns,
- allow interactive manipulation of images and derived products,
- integrate basic analysis functions directly into the visualization interface,
- provide a framework for implementation of custom functions in Python. 

FIST addresses these requirements by providing a lightweight, extensible application that combines interactive visualization with simple analytical tools in a single, browser-based interface. By using a modular architecture and relying on widely adopted open-source libraries, FIST can be readily adapted to new instruments and use cases.

---

## Design and Functionality

FIST runs as a local web application served by Panel, requiring only a standard web browser for interaction. The user interface is composed of a control panel for file selection and parameter adjustment, and a main display area for image visualization.

Key features include:

- visualization of two- and three-dimensional FITS image data, with automatic handling of multi-extension files;
- percentile-based image scaling with selectable stretches, gamma correction, contrast adjustment, and colormap control;
- image transformations such as rotation, axis flips, and negative display;
- arithmetic operations between image products for direct inspection;
- interactive definition of cuts and regions, with real-time display of profiles and basic statistics;
- inspection and filtering of FITS headers in fixed-width format;
- optional monitoring of directories for newly produced files (autofetch mode);
- support for instrument-specific configuration files defining file patterns, extensions, and sourcelet naming.

FIST is distributed with example FITS files and supports a dedicated command-line option to launch the application using bundled example data, facilitating demonstration and testing.

---

## Availability and Reuse

FIST is distributed under the MIT License and is available as an open-source Python package. Installation is performed using standard Python packaging tools. The software is designed to be reusable both as an end-user application and as a foundation for customized visualization or quick-look tools in astronomical research contexts.

---

## Acknowledgements

Pedro Figueira acknowledges financial support from the Severo Ochoa grant CEX2021-001131-S funded by MCIN/AEI/10.13039/501100011033. This work has also received funding from the European Union (ERC, THIRSTEE, 101164189). Views and opinions expressed are those of the author and do not necessarily reflect those of the European Union or the European Research Council.

The author gratefully acknowledges the developers and maintainers of the open-source scientific Python ecosystem, including NumPy, SciPy, Astropy, Bokeh, Panel, and Matplotlib which make this work possible.

---

## References

