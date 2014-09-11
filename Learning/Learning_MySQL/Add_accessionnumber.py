# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 16:14:45 2014

@author: pczrr
"""

import MySQLdb as mdb
import glob
import argparse
import os
import getpass
import subprocess as sub

#def dexport (table):
#    cursor.execute("select Header,Sequence from `" + table_name + "` where `Pol-type` not like 'PolC' into outfile '/tmp/" + table_name + 
#        ".fasta' fields terminated by '\n'" + 
#        "lines starting by '>';")
#
#def alignseq (seqs):
#        sub.check_call("mafft --thread 4 --auto --reorder --legacygappenalty /tmp/" + table_name + ".fasta > " + outputdir + table_name + "_aligned.fasta",shell=True)
#
#def makehmm (msa):
#        sub.check_call("hmmbuild --cpu 4 " + outputdir + table_name + ".hmm " + outputdir + table_name + "_hmmaligned.a2m",shell=True)
#
#def alignhmm (seqs):
#        sub.check_call("hmmalign --trim --informat FASTA --outformat A2M -o " + outputdir + table_name + "_hmmaligned.a2m " + outputdir + template + ".hmm /tmp/" + table_name + ".fasta",shell=True)
#
#def makelogo (hmm):
#    sub.check_call("hmmlogo " + outputdir + table_name + ".hmm > " + outputdir + table_name + ".logo",shell=True)
#
#def load_overall (table_name):
#      cursor.execute("load data local infile '/tmp/" + table_name + ".fasta'" +
#	"replace" +
#	" into table All_nr_sequences" +
#	" fields terminated by '\n'" +
#	" lines starting by '>'" + 
#      " (Header,Sequence);")
#      cursor.execute("update All_nr_sequences set `Pol-type`='DnaE'")
#      connection.commit()
#
#def cleanup (table_name):
#    os.Popen("echo " + password + " | sudo -S rm /tmp/" + table_name + ".fasta",shell=True)

#command line arguments
#parser = argparse.ArgumentParser(description="Create and annotate sequence database of DnaEs")
##parser.add_argument("d", dest="delimiter", required=True,
##                        help="field delimiter", metavar="delimiter")
##parser.add_argument("l", dest="linebreak", required=True,
##                        help="line break character", metavar="linebreak")
#parser.add_argument("src_path", metavar="path", type=str,
#    help="Path to files to be loaded into database; enclose in quotes, accepts * as wildcard for directories or filenames")
#args = parser.parse_args()
##delimiter = args.delimiter
##linebreak = args.linebreak
#files = glob.iglob(args.src_path)
#
#outputdir="/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaE3-alignment/Analysis/HMM_method/HMMsbyPhyla/"
#overallT='All_DnaE_sequences'
#template= overallT

#begin main program
#connect to MySQL server
un = 'pczrr'
password = getpass.getpass()
connection = mdb.connect(host='localhost',db='DnaE_sequences',user=un,passwd=password)
cursor = connection.cursor()

#        

#dexport (overallT)
#print 'All DnaE sequences file assembled'
#raw_input("Press Enter to continue...")
#alignseq (overallT)
#print 'All DnaE sequences alignment made'
#raw_input("Press Enter to continue...")
#makehmm (overallT)
#print 'Overall DnaE HMM construction complete.'

#Create tables with basic columns
#for filename in files:
#    print filename
#    newtable = os.path.splitext(filename)[0]
#    print newtable
#    cursor.execute("create table `" + newtable + "` ("
#    + "`Header` VARCHAR(200) NOT NULL DEFAULT 'Empty',"
#  + "`Sequence` VARCHAR(3000) NOT NULL DEFAULT 'A',"
#  + "`Pol-type` VARCHAR(10) NOT NULL DEFAULT 'DnaE',"
#  + "PRIMARY KEY (`Header`)); ")
#    cursor.execute("load data local infile '" + filename + "' ignore into table " + newtable + 
#    " fields terminated by '\n' " +
#    "lines starting by '>' " +
#    "(Header,Sequence)")
#    connection.commit()

#Flag PolCs
#Begin by labeling all known PolCs
#cursor.execute("update PolC_nr_sequences set `Pol-type`='PolC'")
#connection.commit()

#Clean out fragments, then flag PolCs
cursor.execute("SHOW TABLES")
for (table_name,) in cursor:
        if 'Test' in table_name:
            continue
        cursor.execute("alter table `" + table_name + "` add column `Accession_Number` VARCHAR(10) NOT NULL DEFAULT 'X00000'")        
        cursor.execute("update `" 
        + table_name + "` a set a.`Accession_Number`=left(a.Header,6)")        
        cursor.execute("create index " + table_name + "_AccNum on `" 
        + table_name + "`(Accession_Number)")     
        print table_name +'updated'
        connection.commit()
             
connection.close()