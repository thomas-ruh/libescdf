#!/usr/bin/python3

# This script is meant to be called from the top source directory

import os
import sys

# Add path to ESCDF Python modules before calling them
pkg_dir, x = os.path.split(os.path.abspath(__file__))
pkg_dir = os.path.join(pkg_dir, "python")
sys.path.insert(0, pkg_dir)

from escdf.glue import EscdfFortranGlue
from escdf.fortran import EscdfFortranModule

# Glue file
geo_glue_text = str(EscdfFortranGlue(
    "geometry", "./python/specs/escdf-specs-geometry-0.1.yml"))
geo_glue_file = "./fortran/escdf_f03_geometry.c"
with open(geo_glue_file, "w") as geo_glue:
    geo_glue.write(geo_glue_text)

# Fortran module
geo_mod_text = str(EscdfFortranModule(
    "geometry", "./python/specs/escdf-specs-geometry-0.1.yml"))
geo_mod_file = "./fortran/escdf_geometry.F90"
with open(geo_mod_file, "w") as geo_mod:
    geo_mod.write(geo_mod_text)
