#!/usr/bin/python
#FMT=Fraction Mix Test
##Was working on tying together histogram, fit, and plot fxns
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

def qlpdir(path):
    """
#    Maybe this exists?
#    """
    scQLPs = "c:/Users/rrymer/Documents/Data/"
    return "%s/%s" % (scQLPs, path)

factory = QLNumpyObjectFactory() #not sure what this does

#Lightweight plate, collects all the wells to be analyzed by plate
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
##Collates all plates and wells into a single string
class MultiPlate(object):
    def __init__(self):
        self.plates = {}

    def read_files(self, files):
        self.plates = {}
        cnt=1;
        for filename in files:
            plate = factory.parse_plate(filename)
            wells = plate.analyzed_wells;
            self.add_plate( filename, plate.document_name, cnt ) 
            for wellname in wells:
                self.get_plate( cnt ).add_well( plate.wells[wellname], 1 )
            cnt = cnt + 1;
        return self

    def read_files_from_glob(self, filespec):
        files=[]
        self.plates = {}
        for filename in (glob.glob(filespec ) ):
            files.append( filename )
        self.read_files( files );
        return self

    def has_plate( self, iid ):
        return self.plates.has_key( iid );

    def get_plate( self, iid ):
        return self.plates[iid];

    def add_plate( self, filename, name, id ):
        # SC - need exception is plate exists
        print "add_plate %s" % (filename)
        if self.has_plate( id ):
            print "ERROR - add_plate"
        else:
            self.plates[id]=LWPlate(filename, name)

    def get_well( self, iid, wellname ):
        return self.plates[iid].wells()[wellname]

    def __str__( self ):
        str=""
        for k, lwPlate in self.plates.iteritems():
             str += k + '\n'
             for k, well in lwPlate.wells().iteritems():
                 str += ','.join( well.name ) +'\n'
        return str

class MyController(object):
    def __init__(self, location):
        src_mp = MultiPlate().read_files(location)
        app = mpview(None)
        app.title('my application')
        app.set_global_mp( src_mp )
        app.set_file_src_location( location )
        app.mainloop()


def well_metadata_to_string( well ):
    targets = well.original_targets
    str = "%s\t%s\t%s\t%s" % (well.name, well.original_sample_name, well.original_targets[0], well.original_targets[1] )
    return( str );
    
def well_intensities_to_str( well, plateID ):
    peaks = accepted_peaks(well)
    clusters = well_cluster_peaks( well, None )
    specs = \
        ['negative_peaks', 'negative_peaks', 0, 0], \
        ['negative_peaks', 'positive_peaks', 0, 1], \
        ['positive_peaks', 'negative_peaks', 1, 0],\
        ['positive_peaks', 'positive_peaks', 1, 1]

    intensityStr = ""
    for s in specs:
        x=channel_amplitudes(clusters[s[0]][s[1]], 1)
        y=channel_amplitudes(clusters[s[0]][s[1]], 0)
        z=fam_widths(peaks)
        w=vic_widths(peaks)
        for i in list(range(x.size)):
            tmp = "%s, %s, %d, %d, %d, %d, %d, %d" % ( plateID, well.name, x[i], y[i], s[2], s[3], z[i], w[i] )
            intensityStr = intensityStr +  "\n" + tmp
            
    return intensityStr

def key_for_row_sort( str ):
    # A01, A02, A03, ..., A12, B01, ..., H12
    sep = list( str );
    letter = sep[0]
    num = (int) ( "%s%s" % (sep[1], sep[2] ))
    res = num + 100* ( ord(letter) - ord('A') + 1)
    return res

def key_for_col_sort( str ):
    # A01, B01, C01,...,H01, A02, ..., H12
    sep = list( str );
    letter = sep[0]
    num = (int) ( "%s%s" % (sep[1], sep[2] ))
    res = 100*num + ( ord(letter) - ord('A') + 1)
    return res

def output_well_data( filelist, outname ):
    src_mp = MultiPlate().read_files(filelist)
#        well = src_mp.get_plate(filelist[0]).wells()["A01"]

    global intFile
    intFile = outname + ".intensities.txt"
    wellFile = outname + ".wells.txt"
    plateFile = outname + ".plates.txt"
    intF = open(intFile, "w")
    wellF = open(wellFile, "w")
    plateF = open(plateFile, "w")
    for j, lwPlate in src_mp.plates.iteritems():
        print ( "now reading", lwPlate.filename )
        plateF.write( "%d\t%s\n" % ( j, lwPlate.filename ) )
        for k, well in lwPlate.wells().iteritems():
            intF.write( well_intensities_to_str( well, j ) + "\n" );
            wellF.write( "%d\t%s\t%s\t%s\n" % ( j, well_metadata_to_string( well ), well.channels[0].statistics.concentration, well.channels[1].statistics.concentration ) );
    return intFile
    
##Depreciated function below
##def test( files, outfileBaseName):
##    file1="c:/Users/rrymer/Documents/Data/IC5838P8_060613_fraction.qlp"
##    outtest="test"
##    for f in files:
##        output_well_data(files, outtest )

    #numpy.set_printoptions(threshold="nan")
    #clusters = well_cluster_peaks( well, None )
    #print clusters['negative_peaks']['negative_peaks']


def OutputFiles ( files, outfileBaseName ):
    output_well_data(files, outfileBaseName )
##    test( files, outfileBaseName )

##Add a header (defined later) to the file so it's easier to work with
def AddHeaders( header, intFile ):
    for line in fileinput.input(intFile, inplace=True):
        if fileinput.isfirstline():
            print header,
        print line,
        
##Function to fit the data.  Would like to use something besides least squares.
#class Parameter:
#     def __init__(self, value):
#             self.value = value
# 
#     def set(self, value):
#             self.value = value
# 
#     def __call__(self):
#             return self.value
#
#def fit(function, parameters, y, x):
#     def f(params):
#         i = 0
#         for p in parameters:
#             p.set(params[i])
#             i += 1
#         return y - function(x)
# 
#     p = [param() for param in parameters]
#     optimize.leastsq(f, p)
        
##Calculates a histogram, and fits a gaussian curve
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
    coeff, var_matrix = optimize.curve_fit(f, bin_centers, hist, p_init )
    print  optimize.curve_fit(f, bin_centers, hist, p_init )
    print "this is the fit"
    print coeff
    DFittype = type (coeff)
    print DFittype
    hist_fit = f(bin_centers, *coeff)
    print hist_fit
    return hist_fit

##Calculates the histogram of the data, and plots it along with the fit to a gaussian
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

if __name__ == "__main__":
    script_name = sys.argv[0]
    parser = argparse.ArgumentParser(description="usage: " + script_name + "<image_dir> <pdf out dir>")
##    parser.add_argument("--head", dest="header", help="define header")
    parser.add_argument("--n", dest="outfileBaseName", required=True,
                        help="define output file name", metavar="outfileBaseName")
    parser.add_argument("files", nargs='*')
    args = parser.parse_args()
    header = "plate, wells, VIC.Intensity, FAM.Intensity, FAM.Cluster, VIC.Cluster, FAM.Width, VIC.Width"
    files = args.files
    outfileBaseName = args.outfileBaseName

OutputFiles( args.files, args.outfileBaseName )
print "writing files"
AddHeaders( header, intFile )
data = numpy.genfromtxt(intFile, delimiter=',', skip_header=1)
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
Plot( FAMIntHi, hist_fit )

hist_fit = HistFit( FAMIntLo )
Plot( FAMIntLo, hist_fit )
#PlotHist( VICInt )


    
# python QlpToCSV_DSFractions_6413.py --files="/cygdrive/c/Users/rrymer/Documents/Data/IC5838P8_060613_fraction.qlp" --head="my header" --n="test"

