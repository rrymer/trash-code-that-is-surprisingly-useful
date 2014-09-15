# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 10:58:45 2014

@author: 
"""

import matplotlib
from pylab import *
import numpy as np

data = np.loadtxt('/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaE3-alignment/Analysis/HMM_method/Overall_DnaE_noPolC_FScomparison.txt', converters=None, dtype='float', 
                  delimiter='\t', skiprows=1, usecols=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20))

new_map = matplotlib.colors.LinearSegmentedColormap.from_list('new_map', cmap='RdGy', N=50)
pcolor(data, cmap=new_map, vmin=-4, vmax=4)
colorbar()
savefig('map.png')
show()
