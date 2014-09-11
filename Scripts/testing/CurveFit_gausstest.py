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
    def f(x, height, mean, sd):
        return height*numpy.exp(-(x-mean)**2/(2.*sd**2))
    height = 40000   
    mean = 21000
    sd = 482
    p_init = numpy.array([height, mean, sd])
    Initial_model = f(datax, height, mean, sd)    
    plt.plot(datax, Initial_model, 'b--', label='Initial Model')
    plt.title("Initial vs Fitted Model")
#    plt.title('Initial Model')
   # fit! (given that data is an array with the data to fit)
    print optimize.curve_fit(f, datax, datay, p_init)
    coeff, var_matrix = optimize.curve_fit(f, datax, datay, p_init)
    fit = f(datax, *coeff)
    plt.plot(datax, fit, 'r-')
    plt.show()
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
datax = numpy.array([5116.715,5296.145,5475.575,5655.005,5834.435,6013.865,6193.295,6372.725,6552.155,6731.585,6911.015,7090.445,7269.875,7449.305,7628.735,7808.165,7987.595,8167.025,8346.455,8525.885,8705.315,8884.745,9064.175,9243.605,9423.035,9602.465,9781.895,9961.325,10140.755,10320.185,10499.615,10679.045,10858.475,11037.905,11217.335,11396.765,11576.195,11755.625,11935.055,12114.485,12293.915,12473.345,12652.775,12832.205,13011.635,13191.065,13370.495,13549.925,13729.355,13908.785,14088.215,14267.645,14447.075,14626.505,14805.935,14985.365,15164.795,15344.225,15523.655,15703.085,15882.515,16061.945,16241.375,16420.805,16600.235,16779.665,16959.095,17138.525,17317.955,17497.385,17676.815,17856.245,18035.675,18215.105,18394.535,18573.965,18753.395,18932.825,19112.255,19291.685,19471.115,19650.545,19829.975,20009.405,20188.835,20368.265,20547.695,20727.125,20906.555,21085.985,21265.415,21444.845,21624.275,21803.705,21983.135,22162.565,22341.995,22521.425,22700.855,22880.285])
datay = numpy.array([3,2,1,3,3,4,1,2,0,1,4,1,3,1,4,3,3,2,0,1,4,3,2,0,3,0,3,3,2,4,5,3,3,5,2,2,2,1,1,3,2,0,2,3,4,4,6,3,2,5,5,6,4,1,4,4,1,0,3,5,4,3,5,2,8,3,5,1,8,7,14,20,36,53,66,105,283,869,2510,6458,14181,25379,36950,44842,43603,35706,24698,14300,7575,3042,978,190,35,10,4,4,2,3,0,1])
print datay
print datax

##analyze
fit = Fit( datax, datay )
Plot( datax, datay, fit )
