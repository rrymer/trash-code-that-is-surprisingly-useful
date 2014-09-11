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
    # Calculate histogram
    hist, bin_edges = numpy.histogram(XInt, bins = 100, density=False)
    numpy.array(hist)
    datay = hist
    print "this is the histogram"
    print hist
    print len(hist)
    htype = type(hist)
    print htype
    global bin_centers
    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2
    datax = bin_centers
    print "here are the bin centers"
    print bin_centers
    print len(bin_centers)
    # define your function:
    def f(x, height, mean, sd):
        return height*numpy.exp(-(x-mean)**2/(2.*sd**2))
    XImean = numpy.mean(XInt, axis=0) 
    XIsd = numpy.std(XInt, axis=0)
    height = 40000   
    mean = XImean
    sd = XIsd
    p_init = numpy.array([height, mean, sd])
    Initial_model = f(bin_centers, height, mean, sd)    
    plt.plot(datax, Initial_model, 'b--', label='Initial Model')
    plt.title("Initial vs Fitted Model")
   # fit! (given that data is an array with the data to fit)
    print optimize.curve_fit(f, datax, datay, p_init)
    coeff, var_matrix = optimize.curve_fit(f, datax, datay, p_init)
    fit = f(datax, *coeff)
    plt.plot(datax, fit, 'r-')
    plt.show()
   # fit! (given that data is an array with the data to fit)
    coeff, var_matrix = optimize.curve_fit(f, bin_centers, hist, p_init )
    print  optimize.curve_fit(f, bin_centers, hist, p_init )
    print "this is the fit"
    print coeff
    DFittype = type (coeff)
    print DFittype
    hist_fit = f(bin_centers, *coeff)
    print hist_fit
    return hist_fit

##Calculates the histogram of the data, and plots it along with the fit to a normal mixture (see above)
def Plot( XInt, hist_fit ):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    n, bins, patches = plt.hist(XInt, 100, facecolor='green', alpha=0.75)
    l = ax.plot( bin_centers, hist_fit, 'r-', linewidth=2)
    ax.set_xlabel('Intensity')
    ax.set_ylabel('Droplets')
    ax.set_title("Intensity Histogram")
    ax.autoscale(enable=True, axis='both', tight=None)
    ax.grid(True)
    plt.show()

##Calculates the histogram of the data, and plots it along with the fit to a normal mixture (see above)
    
data = numpy.genfromtxt("C:/Users/rrymer/Documents/Processing/Analysis/71613_FluVerRun/Test.intensities.txt", delimiter=',', skip_header=1)
FAMInt = data[:,3:4]
FAMIntHi = np.extract(FAMInt>=5000, FAMInt)
FAMIntLo = np.extract(FAMInt<=5000, FAMInt)
print "FAM Hi intensities"
print FAMIntHi
print "FAM Lo intensities"
print FAMIntLo

#VICInt = data[:,2:3]
#print VICInt

hist_fit = HistFit( FAMIntHi )
Plot ( FAMIntHi, hist_fit )

#hist_fit = HistFit( FAMIntLo )
