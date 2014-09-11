#!/usr/bin/python
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
from optparse import OptionParser
from pyqlb.nstats.peaks import *


def qlpdir(path):
    """
#    Maybe this exists?
#    """
    scQLPs = "c:/Users/rrymer/Documents/Data/"
    return "%s/%s" % (scQLPs, path)

factory = QLNumpyObjectFactory()
#plate = factory.parse_plate(qlpdir('EvaGreenPPEDNRwBGDNAAttempt3.qlp'))


##Lightweight plate
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
        print ("now reading", filename)

class MultiPlate(object):
    def __init__(self):
        self.plates = {}

    def read_files(self, files):
        self.plates = {}
        cnt=1;
        for filename in files:
            print ("now reading", filename)
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
    print "I am working"
    sep = list( str );
    letter = sep[0]
    num = (int) ( "%s%s" % (sep[1], sep[2] ))
    res = 100*num + ( ord(letter) - ord('A') + 1)
    return res

def output_well_data( filelist, outname ):
    src_mp = MultiPlate().read_files(filelist)
#        well = src_mp.get_plate(filelist[0]).wells()["A01"]

    intFile = outname + ".intensities.txt"
    wellFile = outname + ".wells.txt"
    plateFile = outname + ".plates.txt"
    intF = open(intFile, "w")
    wellF = open(wellFile, "w")
    plateF = open(plateFile, "w")
    for j, lwPlate in src_mp.plates.iteritems():
        plateF.write( "%d\t%s\n" % ( j, lwPlate.filename ) )
        for k, well in lwPlate.wells().iteritems():
            intF.write( well_intensities_to_str( well, j ) + "\n" );
            wellF.write( "%d\t%s\t%s\t%s\n" % ( j, well_metadata_to_string( well ), well.channels[0].statistics.concentration, well.channels[1].statistics.concentration ) );

def test( files, outfileBaseName):
    file1="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_01.qlp"
    file2="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_02.qlp"
    file3="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_04.qlp"
    file4="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_05.qlp"
    file5="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_06.qlp"
    file6="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_08.qlp"
    file7="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_09.qlp"
    file8="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_10.qlp"
    file9="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_11.qlp"
    file10="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_12.qlp"
    file11="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_13.qlp"
    file12="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_14.qlp"
    file13="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_15.qlp"
    file14="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_16.qlp"
    file15="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_17.qlp"
    file16="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_18.qlp"
    file17="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_19.qlp"
    file18="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_20.qlp"
    file19="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_21.qlp"
    file20="c:/Users/rrymer/Documents/Processing/Data/Fraction_Combination_Simulation/QC_FluVer_20130611_22.qlp"
    outtest="plate1_8"
    output_well_data((file1, file2, file3, file4, file5, file6), outtest )
    outtest="plate9_13"
    output_well_data((file7, file8, file9, file10, file11), outtest )
    outtest="plate14_18"
    output_well_data((file12, file13, file14, file15, file16), outtest )
    outtest="plate19_22"
    output_well_data((file17, file18, file18, file19, file20), outtest )

    #numpy.set_printoptions(threshold="nan")
    #clusters = well_cluster_peaks( well, None )
    #print clusters['negative_peaks']['negative_peaks']



if __name__ == "__main__":
    script_name = sys.argv[0]
    parser = OptionParser("usage: " + script_name + "<image_dir> <pdf out dir>")
    (options, args) = parser.parse_args()
    if len(args) < 2:
        parser.error("Not enough arguments")
    outfileBaseName = args[len(args)-1]
    files = args[0:len(args)-2]

    output_well_data(files, outfileBaseName )
    test( files, outfileBaseName )
    
    #location="/Users/scooper/BioRad/QLPs/RMD Content/*.qlp"
    #MyController(location)

