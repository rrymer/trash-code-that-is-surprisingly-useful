# -*- coding: utf-8 -*-
"""
Created on Sat May 31 13:10:31 2014

@author: 
"""

import glob
import itertools
import subprocess as sp
import os

dict = {'DnaA':'/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaA-alignment/Data/',
        'DnaC':'/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaC-alignment/Data/',
        'DnaG':'/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaG-alignment/Data/',
        'DnaB':'/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaB-alignment/Data/',
        }
for n,d in dict.iteritems():
    files = glob.glob('/tmp/*{}*Sequence*'.format(n))
    print len(files)
    for f in files:
        name = os.path.split(f)
        sp.Popen(['mv', f, d + name[1]])
