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
import csv 
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
    
def well_intensities_to_str_wname( well, plateID, platename ):
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
            tmp = "%s, %s, %s, %d, %d, %d, %d" % ( plateID, platename, well.name, x[i], y[i], s[2], s[3] )
            intensityStr = intensityStr +  "\n" + tmp
            
    return intensityStr
    
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

def output_well_data( filelist, outname, label ):
    src_mp = MultiPlate().read_files(filelist)
#        well = src_mp.get_plate(filelist[0]).wells()["A01"]
    global intFile
    global plateFile
    intFile = outname + ".intensities.txt"
    wellFile = outname + ".wells.txt"
    plateFile = outname + ".plates.txt"
    intF = open(intFile, "w")
    wellF = open(wellFile, "w")
    plateF = open(plateFile, "w")
    if 'f' in label:    
        writer = csv.DictWriter(intF, fieldnames = ["plateID", "plate name", "wells", "VIC.Intensity", "FAM.Intensity", "FAM.Cluster", "VIC.Cluster"], delimiter = ',')
    else: writer = csv.DictWriter(intF, fieldnames = ["plateID", "wells", "VIC.Intensity", "FAM.Intensity", "FAM.Cluster", "VIC.Cluster"], delimiter = ',')
    writer.writeheader()
    for j, lwPlate in src_mp.plates.iteritems():
        print "now processing" + lwPlate.filename
        plateF.write( "%d\t%s\n" % ( j, lwPlate.filename ) )
        for k, well in lwPlate.wells().iteritems():
            if "f" in label:
                    intF.write( well_intensities_to_str_wname( well, j, lwPlate.filename ) + "\n" )
            else: intF.write( well_intensities_to_str( well, j ) + "\n" )
            wellF.write( "%d\t%s\t%s\t%s\n" % ( j, well_metadata_to_string( well ), well.channels[0].statistics.concentration, well.channels[1].statistics.concentration ) );
    return intFile

def OutputFiles ( files, outfileBaseName, label ):
    output_well_data(files, outfileBaseName, label )
##    test( files, outfileBaseName )

##Recodes the plate names to match those of the original files
#def Recode ( plateFile ):
#    reader = csv.reader(open(plateFile, 'r'), delimiter='\t')
#    d = {}
#    for row in reader:
#        k, v = row
#        d[k] = v
#    writer = csv.DictWriter(open(intFile, 'w'), fieldnames = ["plate"], delimiter=',')    
#    for row in writer:
#        print row
            
        
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
parser.add_argument("color", type=str,
                    help="Define what colors to examine: FAM+, FAM-, VIC+, VIC-, HEX+, HEX-, or all", metavar="colors")
parser.add_argument("--p", dest="plot", type=str,
                    help="plot the results, y or n", metavar="plot_preference")
parser.add_argument("--l", dest="label", type=str,
                    help="print plate number (n) or file name (f) to file for each droplet ", metavar="label_preference")
                    
args = parser.parse_args()
files = glob.iglob(args.src_path)
outfileBaseName = args.outfileBaseName
color = args.color
plot = args.plot
label = args.label

try:
    files.next()
except StopIteration:
    print "no matching files in source path"
    quit()

OutputFiles( files, outfileBaseName, label )

#print "recoding plate names"
#Recode ( plateFile )

if 'y' in plot.lower():
    try:        
        data = numpy.genfromtxt(intFile, delimiter=',', skip_header=1)
    except StopIteration: 
        print "no files or wrong file type (non QLP)"
        quit()

    if 'f' in color.lower() or 'all' in color.lower():
        FAMInt = data[:,3:4]  
        
    if 'h' in color.lower() or 'v' in color.lower() or 'all' in color.lower():
        VICInt = data[:,2:3]
    
    if 'all' in color.lower() or 'f+' in color.lower() or 'fam+' in color.lower() or 'famhi' in color.lower() or 'fam hi' in color.lower():
        FAMIntHi = np.extract(FAMInt>=5000, FAMInt)
        Title = "FAM Hi"
        hist_fit = HistFit( FAMIntHi )
        Plot( FAMIntHi, hist_fit )
    
    if 'all' in color.lower() or 'f-' in color.lower() or 'famlo' in color.lower() or 'famlo' in color.lower() or 'fam lo' in color.lower():
        FAMIntLo = np.extract(np.logical_and(FAMInt<=5000,FAMInt>=1000), FAMInt)
        Title = "FAM Lo"    
        hist_fit = HistFit( FAMIntLo )
        Plot( FAMIntLo, hist_fit )
    
    if "vic+" in color.lower() or "v+" in color.lower() or "vichi" in color.lower() or "vic hi" in color.lower() or "hex+" in color.lower() or "h+" in color.lower() or "hexhi" in color.lower() or "hex hi" in color.lower() or "all" in color.lower():  
        VICIntHi = np.extract(np.logical_and(VICInt>=5000,VICInt<=15000), VICInt)
        Title = "VIC/HEX Hi"    
        hist_fit = HistFit( VICIntHi )
        Plot( VICIntHi, hist_fit )
        
    if "vic-" in color.lower() or "v-" in color.lower() or "viclo" in color.lower() or "vic lo" in color.lower() or "hex-" in color.lower() or "h-" in color.lower() or "hexlo" in color.lower() or "hex lo" in color.lower() or "all" in color.lower():  
        VICIntLo = np.extract(np.logical_and(VICInt<=5000,VICInt>=1000), VICInt)
        Title = "VIC/HEX Lo"       
        hist_fit = HistFit( VICIntLo )
        Plot( VICIntLo, hist_fit )
else: print "skipping plotting"

print "Done"



# python QlpToCSV_DSFractions_6413.py --files="/cygdrive/c/Users/rrymer/Documents/Data/IC5838P8_060613_fTypeError: expected string or bufferraction.qlp" --head="my header" --n="test"

