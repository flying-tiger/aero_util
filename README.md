# aero_util
A set of utilities supporting vehicle aerodynamic analysis

## Overview
This project provides a collection of utilites that are intended to
make life easier when doing aerodynamic analysis. I have a pretty large
library of scripts that I've written over the years and I will be
migrating them into this toolbox over time. These scripts do things
like:

 * Convert units of measure
 * Perform coordinate system rotations
 * Convert attitude representations (alpha/beta, alphat/phi, etc.)
 * Compute stagnation conditions for calorically perfect gases
 * Compute properties for the US Standard Atmosphere
 * Load and manipulate surface/volume meshes for CFD analysis

For a complete list of the modules in this package, see the end of this
file.

## Requirements

 * Python 3.6+
 * Numpy  1.12+
 * XArray 0.9.6+
 * Pint   0.7.0+

Note: Python 3.6 is a hard requirement, but older version of the library
dependencies may work; the list above is simply the versions used for
development.

## Package Contents

    aero_util
      |- attitude    Compute/convert wind relative attitude angles
      |- grids       Load Plot3D grid files: 2D/3D, single or multi-block

