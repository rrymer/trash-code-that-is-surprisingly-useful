# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 16:14:45 2014

@author: pczrr
"""

import MySQLdb as mdb
import getpass
import subprocess as os
import matplotlib
from pylab import *
import numpy as np
import itertools as it

def dexport (table):
    cursor.execute("select Header,Sequence from `" + table_name + "` where `Pol-type` not like 'PolC' into outfile '/tmp/" + table_name + 
        ".fasta' fields terminated by '\n'" + 
        "lines starting by '>';")

def alignseq (seqs):
        os.check_call("mafft --thread 4 --auto --reorder --legacygappenalty /tmp/" + table_name + ".fasta > " + outputdir + table_name + "_aligned.fasta",shell=True)

def makehmm (msa):
        os.check_call("hmmbuild --cpu 4 " + outputdir + table_name + ".hmm " + outputdir + table_name + "_hmmaligned.a2m",shell=True)

def alignhmm (seqs):
        os.check_call("hmmalign --trim --informat FASTA --outformat A2M -o " + outputdir + table_name + "_hmmaligned.a2m " + outputdir + template + ".hmm /tmp/" + table_name + ".fasta",shell=True)

def makelogo (hmm):
    os.check_call("hmmlogo " + outputdir + table_name + ".hmm > " + outputdir + table_name + ".logo",shell=True)

def load_overall (table_name):
      cursor.execute("load data local infile '/tmp/" + table_name + ".fasta'" +
	"ignore" +
	" into table All_DnaE_sequences" +
	" fields terminated by '\n'" +
	" lines starting by '>'" + 
      " (Header,Sequence);")
      cursor.execute("update All_DnaE_sequences set `Pol-type`='DnaE'")

def cleanup (table_name):
    os.Popen("echo " + password + " | sudo -S rm /tmp/" + table_name + ".fasta",shell=True)

outputdir="/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaE3-alignment/Analysis/HMM_method/HMMsbyPhyla/"
overallT='All_DnaE_sequences'
template= overallT
un = 'pczrr'
password = getpass.getpass()
connection = mdb.connect(host='localhost',db='DnaE_sequences',user=un,passwd=password)

cursor = connection.cursor()
    
cursor.execute("SHOW TABLES")
for (table_name,) in cursor:
        if 'PolC_nr_sequences' in table_name or 'Test' in table_name or 'All' in table_name:
            continue       
        dexport(table_name)
        #load_overall(table_name)
        print table_name + ' exported to fasta'
        
        
go_on = raw_input("continue? (y/n)")
if 'n' in go_on:
    quit

dexport (overallT)
print 'All DnaE sequences file assembled'
raw_input("Press Enter to continue...")
alignseq (overallT)
print 'All DnaE sequences alignment made'
raw_input("Press Enter to continue...")
makehmm (overallT)
print 'Overall DnaE HMM construction complete.'
        
cursor.execute("SHOW TABLES")
for (table_name,) in cursor:
        if 'PolC_sequences' in table_name or 'Test' in table_name or 'All' in table_name:
            continue        
#        alignhmm(table_name)
#        print table_name + ' aligned'
#        makehmm(table_name)
#        print table_name + ' modeled'
#        cleanup(table_name)
#        cleanup (overallT)
        makelogo(table_name)
connection.commit()
connection.close()


#cursor.execute("update `DnaE_sequences`.`Actinobacteria_sequences` set `Pol-type`=defaulcall