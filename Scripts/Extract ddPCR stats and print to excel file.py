# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 13:44:44 2013

@author: rrymer
"""

from pyqlb.factory import QLNumpyObjectFactory
from pyqlb.nstats.peaks import fam_amplitudes
import numpy as np

factory = QLNumpyObjectFactory()

class LWPlate( object ):
    def add_well( self, well, fulldata ):
        # Should throw an exception if wellname exists, but have not figure out perl exception handling yet
        if fulldata:
            self.well_list[well.name] = well
        else:
            self.well_list[well.name] = ""

    def wells(self):
        print self
        return( self.well_list )
        
    def __init__(self, filename, platename):
        self.filename=filename
        self.platename=platename
        self.well_list={}

plate = factory.parse_plate('\\Users\\rrymer\\Documents\\Processing\\Data\\EvaGreenPPEDNRnoBGDNAAttempt3.qlp') # this should be quick!
a01 = plate.analyzed_wells['A01']

mean = np.mean(fam_amplitudes(a01.peaks))
print mean