# -*- coding: utf-8 -*-
"""
Created on Mon Nov 04 11:06:32 2013

@author: rrymer
"""

import argparse
import glob
import os
import fnmatch

parser = argparse.ArgumentParser(description='SO test.')
parser.add_argument("src_path", metavar="path", type=str,
    help="Path to files to be merged; enclose in quotes, accepts * as wildcard for directories or filenames")
#parser.add_argument("file_name", type=str)
args = parser.parse_args()
files = glob.glob(args.src_path)

print files
print args.src_path