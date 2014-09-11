# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 20:47:08 2013

@author: rrymer
"""

from pyqlb.nstats import concentration, concentration_interval, cnv, cnv_interval
from pyqlb.nstats.peaks import *
from pyqlb.nstats.well import *
from pyqlb.factory import QLNumpyObjectFactory
from pyqlb.objects import QLWell, QLWellChannelStatistics
import sys
import glob
import re
import os
import numpy
import fileinput  
import argparse
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy import optimize
from pylab import *
from pyqlb.nstats.peaks import *


#class Parameter:
#     def __init__(self, value):
#             self.value = value
# 
#     def set(self, value):
#             self.value = value
# 
#     def __call__(self):
#             return self.value

#def fit(function, parameters, y, x = None):
#     def f(params):
#         i = 0
#         for p in parameters:
#             p.set(params[i])
#             i += 1
#         return y - function(x)
#         
#     if x is None: x = arange(y.shape[0])
#     p = [param() for param in parameters]
#     print p
#     optimize.leastsq(f, p)
        
##Calculates moments of a guassian, then fits data to a normal mixture model, initial model assumes equal means/sds
def HistFit( XInt ):    
    # giving initial parameters
    hist, bin_edges = numpy.histogram(XInt, bins = 100, density=False)
    print "this is the histogram"
    print hist
#    global bin_centers
    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2
    print "here are the bin centers"
    print bin_centers
#    numpy.ndarray.flatten(XImean)
#    numpy.ndarray.flatten(XIsd)
    # define your function:
#    def f(x): return height() * exp(-((x-mean())/sd())**2.)
    def f(x, *p): 
        p = height, mean, sd       
        return height*numpy.exp(-(x-mean)**2/(2.*sd**2))
    mean = numpy.mean(XInt, axis=0) 
    print mean
    sd = numpy.std(XInt, axis=0) 
    print sd
    height = 10000.
    p0 = [mean, sd, height]
#    mean2 = Parameter(XImean)
#    print mean2
#    sd2 = Parameter(XIsd)
#    print sd2
#    height2 = Parameter(10000.)
#    ratio = Parameter(0.5)
   # p0 = [ratio, mean1, sd1, height1, mean2, sd2, height2]
   # fit! (given that data is an array with the data to fit)
    coeff, var_matrix = optimize.curve_fit(f, bin_centers, hist, p0=p0 )
    hist_fit = f(bin_centers, *coeff)
    n, bins, patches = plt.hist(XInt, 100, facecolor='green', alpha=0.75)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    l = ax.plot( bin_centers, hist_fit, 'r-', linewidth=2)
    ax.set_xlabel('Intensity')
    ax.set_ylabel('Droplets')
    ax.set_title("Intensity Histogram")
    ax.autoscale(enable=True, axis='both', tight=None)
    ax.grid(True)
    plt.show()
#    print "this is the fit"
#    print coeff
#    DFittype = type (coeff)
#    print DFittype
#    global hist_fit
#    hist_fit = f(bin_centers, *coeff)
#    return hist_fit

##Calculates the histogram of the data, and plots it along with the fit to a normal mixture (see above)
    
data = numpy.genfromtxt("C:/Users/rrymer/Documents/Processing/Analysis/71613_FluVerRun/Test.intensities.txt", dtype=float, delimiter=',', skip_header=1)
FAMInt = data[:,3:4]
FAMIntHi = np.extract(FAMInt>=5000, FAMInt)
FAMIntLo = np.extract(FAMInt<=5000, FAMInt)
print "FAM Hi intensities"
print FAMIntHi
print "FAM Lo intensities"
print FAMIntLo

#VICInt = data[:,2:3]
#print VICInt

HistFit( FAMIntHi )


HistFit( FAMIntLo )
