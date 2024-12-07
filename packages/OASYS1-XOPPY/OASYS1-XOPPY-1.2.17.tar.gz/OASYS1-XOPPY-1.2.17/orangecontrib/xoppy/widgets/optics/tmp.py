
#
# script to calculate crystal diffraction profiles (created by XOPPY:crystal)
#

import numpy
from xoppylib.crystals.tools import bragg_calc2, run_diff_pat
import xraylib
from dabax.dabax_xraylib import DabaxXraylib

#
# run bragg_calc (preprocessor) and create file xcrystal.bra
#
bragg_dictionary = bragg_calc2(
    descriptor = "Si",
    hh         = 1,
    kk         = 1,
    ll         = 1,
    temper     = 1.0,
    emin       = 59900.0,
    emax       = 60100.0,
    estep      = 0.4,
    ANISO_SEL  = 0,
    fileout    = "xcrystal.bra",
    do_not_prototype = 0,  # 0=use site groups (recommended), 1=use all individual sites
    verbose = False,
    material_constants_library = xraylib,
    )

#
# run external (fortran) diff_pat (note that some parameters may not be used)
#
run_diff_pat(
    bragg_dictionary,
    preprocessor_file  = "xcrystal.bra",
    descriptor         = "Si",
    MOSAIC             = 3,
    GEOMETRY           = 1,
    SCAN               = 2,
    UNIT               = 1,
    SCANFROM           = -200.0,
    SCANTO             = 200.0,
    SCANPOINTS         = 200,
    ENERGY             = 60000.0,
    ASYMMETRY_ANGLE    = 80.0,
    THICKNESS          = 0.05,
    MOSAIC_FWHM        = 0.1,
    RSAG               = 125.0,
    RMER               = 12900.0,
    ANISOTROPY         = 1,
    POISSON            = 0.22,
    CUT                = "2 -1 -1 ; 1 1 1 ; 0 0 0",
    FILECOMPLIANCE     = "mycompliance.dat",
    )

#
# example plot
#
from srxraylib.plot.gol import plot
data = numpy.loadtxt("diff_pat.dat", skiprows=5)
plot(data[:,0], data[:,-1], data[:,0], data[:,-2], ytitle='Crystal reflectivity', legend=['s-polarization','p-polarization'])

#
# end script
#
