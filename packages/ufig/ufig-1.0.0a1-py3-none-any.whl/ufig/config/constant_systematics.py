# Copyright (C) 2013 ETH Zurich, Institute for Astronomy

"""
Created on Jun 11, 2014

author: jakeret
"""

from ufig.config import common

plugins = [
    "ufig.plugins.initialize",
    "ufig.plugins.random_catalog",
    "ufig.plugins.add_lensing",
    "ufig.plugins.add_psf",
    "ufig.plugins.gamma_interpolation_table",
    "ufig.plugins.render_galaxies",
    "ufig.plugins.show_render_galaxies_stats",
    "ufig.plugins.render_stars",
    "ufig.plugins.show_render_stars_stats",
    "ufig.plugins.convert_photons_to_adu",
    "ufig.plugins.saturate_pixels",
    "ufig.plugins.background_noise",
    "ufig.plugins.resample",
    "ufig.plugins.background_subtract",
    "ufig.plugins.write_catalog",
    "ufig.plugins.write_image",
    "ufig.plugins.run_sextractor",
    "ufig.plugins.load_sextractor_catalog",
    "ufig.plugins.match_sextractor_catalog",
    "ivy.plugin.show_stats",
]


for name in [name for name in dir(common) if not name.startswith("__")]:
    globals()[name] = getattr(common, name)
