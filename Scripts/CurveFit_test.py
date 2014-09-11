# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 20:47:08 2013

@author: rrymer
"""


import numpy
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy import optimize

##Fit
def Fit( datax, datay ):    
    # define your function:
    def f(x, m, b):    
        return m*x + b
    m = 0.4
    b = 2.4
    p_init = numpy.array([m, b])
    Initial_model = f(datax, m, b)    
    plt.plot(datax, Initial_model, label='Initial Model')
    plt.title("Initial Model")
#    plt.title('Initial Model')
   # fit! (given that data is an array with the data to fit)
    print optimize.curve_fit(f, datax, datay, p_init)
    coeff, var_matrix = optimize.curve_fit(f, datax, datay, p_init)
    fit = f(datax, *coeff)
    plt.plot(datax, fit, 'r-')
    plt.show()
    print 'Fitted slope 1 = ', coeff[0]
    print 'Fitted intercept 1 = ', coeff[1]
    return fit

##Plot
def Plot( datax, datay, fit ):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(datax, datay, 'b*')
    l = ax.plot( datax, fit, 'r-', linewidth=2)
    ax.set_xlabel('Rate')
    ax.set_ylabel('Return')
    ax.set_title("Test")
    ax.autoscale(enable=True, axis='both', tight=None)
    ax.grid(True)
    plt.show()

##data
datax = numpy.array([7.02, 20.06, 13.78, 16.92, 10.17])
datay = numpy.array([5.14, 10.66, 8.44, 9.64, 6.79])
print datay
print datax

##analyze
fit = Fit( datax, datay )
Plot( datax, datay, fit )
