from pyqlb import *
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
    Maybe this exists?
    """
    scQLPs = "/Users/scooper/BioRad/QLPs/RMD Content/*.qlp"
    return "%s/%s" % (scQLPs, path)


factory = QLNumpyObjectFactory()
#plate = factory.parse_plate(qlpdir('BHQ content_WeiY_Annealing_T_55C_Panel_1.qlp'))
#duplex = factory.parse_plate(qlpdir('BHQ content_WeiY_Annealing_T_55C_Panel_2.qlp'))
#old_style = factory.parse_plate(qlpdir('BHQ content_WeiY_Annealing_T_55C_Panel_1.qlp'))



# Lightweight plate
class LWPlate( object ):
    def add_well( self, well, fulldata ):
        # Should throw an exception if wellname exists, but have not figure out perl exception handling yet
        if fulldata:
            self.well_list[well.name] = well
        else:
            self.well_list[well.name] = ""

    def wells(self):
        return( self.well_list )
        
    def __init__(self, filename, platename):
        self.filename=filename
        self.platename=platename
        self.well_list={}
        

class MultiPlate(object):
    def __init__(self):
        self.plates = {}

    def read_files(self, files):
        self.plates = {}
        cnt=1;
        for filename in files:
            print( filename )
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
        #print "add_plate %s" % (filename)
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
        #well = src_mp.get_plate(filelist[0]).wells()["A01"]

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
    file1="/Users/scooper/BioRad/QLPs/RMD Phase II/RMDContent2 _WeiY_070513_RMD-TG_Plate1.qlp"
    file2="/Users/scooper/BioRad/QLPs/RMD Phase II/RMDContent2 _WeiY_070513_RMD-TG_Plate2.qlp"
    outtest="outFileTest"
    output_well_data((file1, file2), outtest )

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
    #test( files, outfileBaseName )
    
    #location="/Users/scooper/BioRad/QLPs/RMD Content/*.qlp"
    #MyController(location)

