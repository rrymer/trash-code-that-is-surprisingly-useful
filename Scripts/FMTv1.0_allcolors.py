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
        for i in list(range(x.size)):
            tmp = "%s, %s, %d, %d, %d, %d" % ( plateID, well.name, x[i], y[i], s[2], s[3] )
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

def OutputFiles ( files, outfileBaseName ):
    output_well_data(files, outfileBaseName )
##    test( files, outfileBaseName )

##Add a header (defined later) to the file so it's easier to work with
def AddHeaders( header, intFile ):
    for line in fileinput.input(intFile, inplace=True):
        if fileinput.isfirstline():
            print header,
        print line,
        
#Calculates a histogram, and fits a gaussian curve
def HistFit( XInt ):    
    # Calculate histogram
    hist, bin_edges = numpy.histogram(XInt, bins = 100, density=False)
    numpy.array(hist)
    datay = hist
    global bin_centers
    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2
    datax = bin_centers
    # define your function:
    def f(x, height, mean, sd):
        return height*numpy.exp(-(x-mean)**2/(2.*sd**2))
    global mean, sd, CV
    mean = numpy.mean(XInt, axis=0) 
    sd = numpy.std(XInt, axis=0)
    CV = sd/mean
    print mean, sd, CV
    height = 40000   
    p_init = numpy.array([height, mean, sd])
    Initial_model = f(bin_centers, height, mean, sd)    
    plt.plot(datax, Initial_model, 'b--', label='Initial Model')
    plt.title("Initial vs Fitted Model")
   # fit! (given that data is an array with the data to fit)
    coeff, var_matrix = optimize.curve_fit(f, bin_centers, hist, p_init )
    print  optimize.curve_fit(f, bin_centers, hist, p_init )
    print "this is the fit"
    print coeff
    mean = coeff[1]
    sd = coeff[2]
    print mean, CV
    hist_fit = f(bin_centers, *coeff)
    return hist_fit

##Calculates the histogram of the data, and plots it along with the fit to a gaussian
def Plot( XInt, hist_fit ):
    current_mean = mean.astype('|S7')
    current_CV = CV.astype('|S5')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    n, bins, patches = plt.hist(XInt, 100, facecolor='green', alpha=0.75)
    l = ax.plot( bin_centers, hist_fit, 'r-', linewidth=2)
    ax.set_xlabel('Intensity')
    ax.set_ylabel('Droplets')
    ax.set_title(Title + " Intensity Histogram\n" + "mean=" + current_mean + " CV=" + current_CV)
    ax.autoscale(enable=True, axis='both', tight=None)
    ax.grid(True)
    plt.show()


parser = argparse.ArgumentParser(description="combine droplets populations")
parser.add_argument("--n", dest="outfileBaseName", required=True,
                        help="define output file name", metavar="outfileBaseName")
parser.add_argument("src_path", metavar="path", type=str,
    help="Path to files to be merged; enclose in quotes, accepts * as wildcard for directories or filenames")
parser.add_argument("color", dest="color", required=True, type=str,
                    help="Define what colors to examine: FAM+, FAM-, VIC+, VIC-, HEX+, HEX-, or all")
args = parser.parse_args()
header = "plate, wells, VIC.Intensity, FAM.Intensity, FAM.Cluster, VIC.Cluster, FAM.Width, VIC.Width"
files = glob.iglob(args.src_path)
outfileBaseName = args.outfileBaseName

OutputFiles( files, outfileBaseName )
print "writing files"
header = "plate, wells, VIC.Intensity, FAM.Intensity, FAM.Cluster, VIC.Cluster, FAM.Width, VIC.Width"
AddHeaders( header, intFile )
data = numpy.genfromtxt(intFile, delimiter=',', skip_header=1)

if ("f" or "all") in color.lower:
    FAMInt = data[:,3:4]

if ("v" or "h" or "all") in color.lower:
    VICInt = data[:,2:3]

if color.lower==("fam+" or "f+" or "famhi" or "fam hi" or "all") is true:
    FAMIntHi = np.extract(FAMInt>=5000, FAMInt)
    Title = "FAM Hi"
    hist_fit = HistFit( FAMIntHi )
    Plot( FAMIntHi, hist_fit )

if color.lower==("fam-" or "f-" or "famlo" or "fam lo" or "all") is true:
    FAMIntLo = np.extract(np.logical_and(FAMInt<=5000,FAMInt>=1000), FAMInt)
    Title = "FAM Lo"
    hist_fit = HistFit( FAMIntLo )
    Plot( FAMIntLo, hist_fit )

if color.lower==("vic+" or "v+" or "vichi" or "vic hi" or "hex+" or "h+" or "hexhi" or "hex hi" or "all") is true:   
    VICIntHi = np.extract(np.logical_and(VICInt>=5000,VICInt<=15000), VICInt)
    Title = "VIC/HEX Hi"
    hist_fit = HistFit( VICIntHi )
    Plot( VICIntHi, hist_fit )
    
if color.lower==("vic-" or "v-" or "viclo" or "vic lo" or "hex-" or "h-" or "hexlo" or "hex lo" or "all") is true:  
    VICIntLo = np.extract(np.logical_and(VICInt<=5000,VICInt>=1000), VICInt)
    Title = "VIC/HEX Lo"
    hist_fit = HistFit( VICIntLo )
    Plot( VICIntLo, hist_fit )

print "Done"


    
# python QlpToCSV_DSFractions_6413.py --files="/cygdrive/c/Users/rrymer/Documents/Data/IC5838P8_060613_fTypeError: expected string or bufferraction.qlp" --head="my header" --n="test"

