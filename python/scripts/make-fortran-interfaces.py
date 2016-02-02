#!/usr/bin/python3

from escdf.fortran import EscdfFortranModule

geo_mod = EscdfFortranModule("geometry", "./specs/escdf-specs-geometry-0.1.yml")
print(geo_mod)
