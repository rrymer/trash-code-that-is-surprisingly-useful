# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 16:14:45 2014

@author: pczrr
"""

import MySQLdb as mdb
import subprocess as os

outputdir="/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaE3-alignment/Analysis/HMM_method/HMMsbyPhyla/"
overallT='All_sequences'
template= outputdir + overallT + '.hhm'

connection = mdb.connect(host='localhost',db='DnaE_sequences',user='pczrr',passwd='Roble8002~')

cursor = connection.cursor()

def dexport (table_name):
    cursor.execute("select Header,Sequence from `" + table_name + "` where `Pol-type` not like 'PolC' into outfile '/tmp/" + table_name + 
        ".fasta' fields terminated by '\n'" + 
        "lines starting by '>';")

def alignseq (table_name):
        os.check_call("mafft --thread 4 --auto --reorder /tmp/" + table_name + ".fasta > " + outputdir + table_name + "_aligned.fasta",shell=True)

def makehmm (table_name):
        os.check_call("hhmake -i " + outputdir + table_name + "_aligned.fasta -o " + outputdir + table_name + ".hhm",shell=True)

def alignhmm (table_name):
        os.check_call("hhalign -i " + outputdir + table_name + ".hhm -t " + template + " -o " + outputdir + table_name + "_hhmaligned.hhm -png " + outputdir + table_name + "_hmmaligned_dotplot.png",shell=True)

#def makelogo (table_name):
#    os.check_call("hhalign -i" + outputdir + table_name + ".hhm -t " + template + "-o " + outputdir + table_name + "_hhmaligned.fasta -ofas",shell=True)

def load_overall (table_name):
      cursor.execute("load data local infile '/tmp/" + table_name + ".fasta'" +
	"replace" +
	" into table All_sequences" +
	" fields terminated by '\n'" +
	" lines starting by '>'" + 
      " (Header,Sequence);")
      cursor.execute("update All_sequences set `Pol-type`='DnaE'")
      connection.commit()

def cleanup (table_name):
    os.Popen("echo | sudo -S rm /tmp/" + table_name + ".fasta",shell=True)
    
cursor.execute("SHOW TABLES")
for (table_name,) in cursor:
        if 'PolC_sequences' in table_name or 'Test' in table_name or 'All' in table_name:
            continue
        print table_name        
        dexport(table_name)
#        load_overall(table_name)
        print table_name + ' exported to fasta'
#        
#go_on = raw_input("continue? (y/n)")
#if 'n' in go_on:
#    quit
#
#dexport (overallT)
#print 'All DnaE sequences file assembled'
#raw_input("Press Enter to continue...")
#alignseq (overallT)
#print 'All DnaE sequences alignment made'
#raw_input("Press Enter to continue...")
#cleanup (overallT)
#makehmm (overallT)
#print 'Overall DnaE HMM construction complete.'
        
cursor.execute("SHOW TABLES")
for (table_name,) in cursor:
        if 'PolC_sequences' in table_name or 'Test' in table_name or 'All' in table_name:
            continue        
        alignseq(table_name)
        print table_name + ' aligned'
        cleanup(table_name)
        makehmm(table_name)
        print table_name + ' modeled'
        alignhmm(table_name)
        print table_name + ' hmm aligned'
connection.close()

#cursor.execute("update `DnaE_sequences`.`Actinobacteria_sequences` set `Pol-type`=defaulcall
