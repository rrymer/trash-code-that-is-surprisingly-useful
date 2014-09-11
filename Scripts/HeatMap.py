# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 10:58:45 2014

@author: pczrr
"""

import heatmap
from pylab import *
import numpy as np
import random

if __name__ == "__main__":
    pts= []
    for x in range(400):
        pts.append((random.random(), random.random() ))
    
    hm = heatmap.Heatmap()
    img = hm.heatmap(pts)
    img = hm.heatmap(datat)
    img.save("~/Documents/classic.png")

#data = np.loadtxt('/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaE3-alignment/Analysis/HMM_method/Overall_DnaE_noPolC_FScomparison.txt', converters=None, dtype='float', 
#                  delimiter='\t', skiprows=1, usecols=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20))
#
#datat = list(map(tuple,data))
#print datat[0]
#
#img = hm.heatmap(datat)
#img.save("~/Documents/classic.png")