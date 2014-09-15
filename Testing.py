# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 11:29:05 2014

@author: 
"""
#import numpy as np
#import itertools as it
#import os
#import matplotlib as plt
#from pylab import *
#import subprocess as sp
#import os
#import glob
#import splinter
import MySQLdb as mdb
import sys
import uniprot
import re
import time
import itertools
import glob
import logging
import os
import html2text
import urllib
from Bio.SubsMat import MatrixInfo as matlist
from Bio import pairwise2 as align
import operator
from cStringIO import StringIO
from Bio.Align.Applications import MafftCommandline
from Bio import AlignIO
import fileinput
from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import
from SOAPpy import WSDL
import subprocess as sp
import numpy as np
import decimal

#table_name='Actinobacteria_sequences'
#
#os.Popen("echo | sudo -S rm /tmp/" + table_name + ".fasta",shell=True)
def connect_to_mysqdb(host, db, un):
    connection = mdb.connect(host=host,db=db,user=un)
    return connection

outputdir="/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaE3-alignment/Analysis/HMM_method/Sequence_Clusters_byPoltype/"
#with open(outputdir + 'All_GapasXs.logo', 'r') as f:    
#    name = os.path.split(f)[0]
#    print name
#    lines = it.islice(f, 2, 11777)
#    master_array = np.genfromtxt(lines, usecols=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21),dtype=
#    (int,float16,float16,float16,float16,float16,float16,float16,float16,float16,float16,float16,float16,float16,float16,float16,float16,float16,float16,float16,float16,float16,float16))
#np.savetxt(outputdir + 'master_array.txt', master_array, delimiter='\')
    
# Make plot with vertical (default) colorbar

#cdict = {'red': ((0.0, 0.0, 0.0),
#                 (0.5, 1.0, 0.7),
#                  (1.0, 1.0, 1.0)),
#          'green': ((0.0, 0.0, 0.0),
#                    (0.5, 1.0, 0.0),
#                    (1.0, 1.0, 1.0)),
#          'blue': ((0.0, 0.0, 0.0),
#                  (0.5, 1.0, 0.0),
#                   (1.0, 0.5, 1.0))}
#my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,256)
#pcolor(rand(10,10),cmap=my_cmap)
#colorbar()

#os.Popen(['perl', '/Users/pczrr/Google Drive/Coding/Scripts/Fasta2Phylip.pl', outputdir + 'AllAligned_seq.fasta', outputdir + 'All_aligned.txt'])
#from Bio.Align.Applications import MafftCommandline
#in_file = '/tmp/test.txt'
#mafft_cline = MafftCommandline(input=in_file, auto=True, reorder=True)
#print mafft_cline
#stdout, stderr = mafft_cline()
#handle = open("/tmp/output.txt", "w")
#handle.write(stdout)
#handle.close()
#p = os.Popen(['phyml', '-i', outputdir + 'DnaE_only_alignment_subset_2_aligned.phy', '-d', 'aa', '-q','--no_memory_check','--quiet', '-u', outputdir + 'DnaE_only_alignment_subset_1_aligned.phy_phyml_tree.txt'])
#p.wait()
#print 'works!'
#trees = glob.iglob(outputdir + '*phyml_tree.txt')
#with open(outputdir + 'compiledtrees.txt', 'w') as outfile:     
#    for t in trees:
#        if os.path.getsize(t) <= 0:
#            continue
#        print 'appending ' + os.path.splitext(os.path.split(t)[1])[0] + ' to compiled tree file.'
#        with open(t) as infile:        
#            outfile.write(infile.read())
#from splinter import Browser
#browser = Browser()
#browser.visit('http://www.ibi.vu.nl/programs/shmrwww/')
#browser.find_by_name('Browse...').first.click()
#browser.attach_file('file', '/tmp/iDnaG_alignment_firms.fasta')
#
#def fib(n):
#    a, b = 0, 1
#    while a < n:
#        print a
#        a, b = b, a+b
#fib(1e100)
#column='Aligned_seq'
#table='Test'
#ratio=0.9
#print type(ratio)
#print ratio
#def function(table,column,ratio):
#    i=1
#    cursor.execute("select avg(length(`" + column + "`)) from `" + table + "`")
#    n=cursor.fetchone()[0]
#    n=str(n)
#    n=float(n)
#    print n
#    cursor.execute("select count(*) from`" + table + "` where `" + column + "` is not Null")
#    cutoff=int(cursor.fetchone()[0])
#    print cutoff
#    cursor.execute("select substring(" + column + ", " + str(i) + ",  1), count(*) from `" + table + "` group by substring(" + column + ", " + str(i) + ",  1)")
#    results = dict(cursor.fetchall())
#    count = results['-']
#    l = []
#    l.append(count)
#    return l
#
##l = function(table,column,0.9)
##print l
#
#cursor.execute("select avg(length(gfAligned_seq)) from DnaGs")
#length = int(cursor.fetchone()[0])
#print length
#print type(length)
#cursor.execute("select * from DnaGs where PolGroup like 'oddDnaG' into outfile '/tmp/oddDgs.dat' fields terminated by '\t'")
#def cli_progress_test(end_val, bar_length=20):
#    for i in xrange(0, end_val):
#        percent = float(i) / end_val
#        hashes = '=' * int(round(percent * bar_length))
#        spaces = ' ' * (bar_length - len(hashes))
#        sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
#        sys.stdout.flush()
#j=1
#while j<=10:
#    cli_progress_test(j, bar_length=20)
#    j=j+1
#
   
#cursor.execute("select Accession_Number, '1' from RepPols")
#numrows=cursor.rowcount
#fucking_finally = dict(cursor.fetchall())
#l =[]
#for k,v in fucking_finally.iteritems():
#    l.append(k)
#iters = itertools.combinations(l, 100)
#for i in iters:
##        print [i]
#    results=uniprot.fetch_uniprot_metadata(i)
#    time.sleep(0.0001)
#    non_decimal = re.compile(r'[^\d.]+')
#    for k,v in results.iteritems():    
#        orgID = non_decimal.sub('', results[k]['TaxID'])
#        name = results[k]['id']
#        print orgID + ' ' + name

#if __name__ == '__main__':
#    basedir='/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/'
#    tables = ['DnaA','DnaB','DnaCI','DnaD']    
#    for t in tables:
#        print 'assembling ' + t + ' sequence database'        
#        f = glob.glob(basedir+t+'-alignment/Data/*.txt')
#        print f[0]
#        print 'Completed assmebly of ' + t + ' sequence database.'

def fetch_and_assign_taxids(seq,table):
    non_decimal = re.compile(r'[^\d.]+') 
    results=uniprot.fetch_uniprot_metadata(seq)
    time.sleep(1)
    connection = mdb.connect(host='localhost',db='FamilyCpolymerases',user='sequser')
    cursor=connection.cursor()
    for k,v in results.iteritems():  
        TaxID = non_decimal.sub('', results[k]['TaxID'])
        ID = results[k]['id']
        k=repr(k)
        print 'IDs:{} {} {}'.format(k,TaxID,ID)
#    TaxID = non_decimal.sub('', results[seq[0]]['TaxID'])
#    ID = results[seq[0]]['id']
#        sql='select * from `{}` where `Accession_Number` like {}'
#        print sql.format(table,repr(k))
#        cursor.execute(sql.format(table,repr(k)))
#        rows=cursor.fetchall()
#        print rows
        sql="update {} set {}='{}' where Accession_Number={}"
        print sql.format(table,'`OrganismID`',TaxID,k)
        cursor.execute(sql.format(table,'`OrganismID`',TaxID,k))
        print sql.format(table,'`Entry_Name`',ID,k)
        cursor.execute(sql.format(table,'`Entry_Name`',ID,k))
        connection.commit()
        time.sleep(1) 
    connection.close()

def create_table(name):
    connection = mdb.connect(host='localhost',db='FamilyCpolymerases',user='sequser')
    cursor=connection.cursor() 
    print 'assembling ' + name + ' sequence database'    
    sql=("CREATE TABLE `%s` (" +
      "`NCBI_GI` varchar(12) DEFAULT NULL," +
      "`Organism` varchar(200) DEFAULT NULL,"+
      "`PolGroup` varchar(45) DEFAULT NULL,"+
      "`Domains` varchar(45) DEFAULT NULL,"+
      "`Phylum` varchar(45) DEFAULT NULL,"+
      "`Class` varchar(45) DEFAULT NULL,"+
      "`Length` int(5) DEFAULT NULL,"+
      "`Sequence` longtext,"+
      "`Header` varchar(200) NOT NULL DEFAULT 'No entry',"+
      "`Accession_Number` varchar(8) DEFAULT 'X00000',"+
      "`OrganismID` varchar(12) DEFAULT NULL,"+
      "`Entry_Name` varchar(45) DEFAULT NULL,"+
      "`Lineage` varchar(90) DEFAULT NULL,"+
      "`Aligned_seq` varchar(10000) DEFAULT NULL,"+
      "`gfAligned_seq` varchar(10000) DEFAULT NULL,"+
      "`Aligned_seq_index` varchar(10000) DEFAULT NULL,"+
      "`Indexing` int(11) DEFAULT '0',"+
      "`gfAligned_seq_index` varchar(10000) DEFAULT NULL,"+
      "`gfAligned_seq_coords` longtext,"+
      "`PolProfile` varchar(45) DEFAULT NULL,"+
      "PRIMARY KEY (`Header`)"+
      ") ENGINE=InnoDB DEFAULT CHARSET=latin1;")
    sql = sql % name
    cursor.execute(sql)
    connection.commit()
    connection.close()

class Logger():
    logger= None
    def myLogger(self,path):
        if None == self.logger:
            self.logger=logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)
            handler=logging.FileHandler('{}/Build_DNARep_seqDB.log'.format(path))
            formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        return self.logger     

def add_header( header, intFile ):
    for line in fileinput.input(intFile, inplace=True):
        if fileinput.isfirstline():
            print '\n',
        print line,
    for line in fileinput.input(intFile, inplace=True):
        if fileinput.isfirstline():
            print header,
        print line,
#args1=['name']
#sql1='select Accession_Number,{} from `{}` where `Sequence` is not null'
#table="DnaAs"
#sql1 = sql1.format('Null',table)
#print sql1
#
#def split_every(n, iterable):
#    i = iter(iterable)
#    piece = list(itertools.islice(i, n))
#    while piece:
#        yield piece
#        piece = list(itertools.islice(i, n))
#
#cursor.execute(sql1)
#seqs = dict(cursor.fetchall())
#connection.close()
#seqs_list = []
#for k,v in seqs.iteritems():
#    seqs_list.append(k)
#seqs = split_every(100,seqs_list)
#i=1
#for seq in seqs:
#    fetch_and_assign_taxids(seq,table)
#seq=['G8X510']
#results=uniprot.fetch_uniprot_metadata(seq)
#print results

#cursor.execute('show tables')
#for table in cursor:
#    print table
#cursor.info()
#for c in cursor:
#    print c

#cursor.execute("select PolGroup,count(*) from RepPols where PolGroup like '%' group by PolGroup")
#results=dict(cursor.fetchall())
#print results
#for k,v in results.iteritems():
#    print '{} {}'.format(str(k),str(v))
#basedir='/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/'
#loggers = Logger()
#logger = loggers.myLogger(basedir)
#logger.debug('start test')
#files = glob.iglob('{}{}-alignment/Data/*'.format(basedir,'DnaA'))
#for f in files:
#    logger.debug(f)
#    logger.debug(os.path.splitext(f)[0])
#    logger.debug(os.path.splitext(f)[1])    
#connection.close()
#x=logging._handlers.copy()
#for i in x:
#    logger.RemoveHandler(i)
#    i.flush()
#    i.close()

#path=urllib.url2pathname('http://zeus.few.vu.nl/jobs/2a5662e1fc2be78609f80ff90f145125/SH.out')
#html = urllib.urlopen(path).read()
#print html2text.html2text(html)

#def pairwise(ref_seq,query_seq):
#    matrix = matlist.blosum62
#    alignments = align.align.globaldx(ref_seq,query_seq,matrix)
#    return alignments
#    

#cursor.execute("select Accession_Number, Sequence from DnaAs where Accession_Number = 'P03004'")
#ref_seq=dict(cursor.fetchall())
#cursor.execute("select Accession_Number, Sequence from DnaAs where OrganismID = '936156'")
#query_seqs = dict(cursor.fetchall())
#max_hits={}
#for k,v in query_seqs.iteritems():
#    score_list=[]
#    algnmt = pairwise(ref_seq['P03004'],v)
#    for a in algnmt:
#        score_list.append(a[2])
#    top_hit = max(score_list)
#    print top_hit
#    max_hits[k]=top_hit
#connection.close()
#print max_hits
#print max(max_hits.iteritems(), key=operator.itemgetter(1))[1]


#with open('/tmp/test.fasta','r') as inF:
#    for line in f.readline():
#        if '>' in line:
#            ID=line[-6:]

#cnt = itertools.count(start=0,step=1)
#cnter = itertools.count(start=0,step=2)
#old_stdout = sys.stdout
#mystdout = StringIO()
#sys.stdout = mystdout
#data = {}
#cnt.next()
#print type(cnt)
#cnter.next()
#print cnter
#i=0
#n=0
#while n < 100:
#    data[i] = n
#    print data
#    n=cnt.next()
#    i=cnter.next()
#sys.stdout = sys.__stdout__
#for line in iter(mystdout.readlines()):
#    print line
#with open('/tmp/test.txt','a') as outfile:
#    outfile.write(mystdout_string)
               
#mafft_out= mafft_cline()
#alignment = {}
#print  mafft_out
#print type(mafft_out)
#for line in iter(mafft_out.getvalue()):
#    seq= ''
#    header=''
#    while '>' not in line:
#        print line
#        seq.append(line)
#    else:
#        header.append(line)
#    alignment[header]=seq
#print alignment
#with open('/tmp/test_aligned.txt', 'w') as handle:
#    handle.write(stdout)
key_field='Header'
seq_field='Sequence'
ID_field='Accession_Number'
name='test0'
tmp_dir='/tmp/'
cnt_dict={}
data_array=np.array([name,0,0,0,0,'a', 0, 'b'])
path='/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNaA-Replication/Processing/scratch/'
in_file = '/tmp/test0.txt'
d = decimal.Decimal(1.1)
#mafft_cline = MafftCommandline(input=in_file, auto=True, reorder=True)
#stdout, stderr = mafft_cline()
#create_table(name)
#connection = mdb.connect(host='localhost',db='FamilyCpolymerases',user='sequser')
#cursor=connection.cursor()
#algnt = AlignIO.read(StringIO(stdout),'fasta')
##alignd = {}
#print algnt
#for record in algnt:
#    print 'inserting record {} into db'.format(str(record.id)[:6])
##    print record.seq
#    cursor.execute("insert ignore into {} (Accession_Number,Header,Sequence) values('{}','{}','{}')"
#    .format(name,str(record.id)[:6],str(record.id),str(record.seq)))
#    connection.commit()
#print 'check db'
#expsql="select {},{} from {} into outfile '{}' fields terminated by '{}' {}"
#print 'exporting fasta'
#print expsql.format(key_field, seq_field, name, tmp_dir + name + '_aligned.fasta','\n',"lines starting by '>'")
#cursor.execute(expsql.format(key_field, seq_field, name, tmp_dir + name + '_aligned.fasta','\n',"lines starting by '>'"))
#print 'export phylip'
#print expsql.format(ID_field, seq_field, name, tmp_dir + name + '_aligned.phy','\t','')
#cursor.execute(expsql.format(ID_field, seq_field, name, tmp_dir + name + '_aligned.phy','\t',''))
#cursor.execute("select max(length({})),count(*) from {}".format(seq_field,name))
#params=cursor.fetchall()
#header = "{}\t{}".format(params[0][1],params[0][0])
#add_header("{}\t{}".format('20','967'),'/tmp/test0_aligned.phy')
#cursor.execute("select count(*) from {} where {} like '%Reference%'".format(name,key_field))
#ref_cnt=cursor.fetchall()
#print params
#print ref_cnt
#cnt_dict[name]=(int(params[0][1])-int(ref_cnt[0][0]),int(ref_cnt[0][0]))
#print cnt_dict
#cursor.execute("truncate {}".format(name))
#cursor.execute("drop table {}".format(name))
#connection.commit()
#connection.close()
#def run_mh(algnt,name,data_array):
#     groupsizes='10 10'
#     p=sp.Popen(['perl', '/Users/pczrr/Google Drive/Coding/Scripts/mh_run.pl', algnt,'--groups', groupsizes],stdout=sp.PIPE)
#     results = p.stdout
#     for line in iter(results):
#        if 'Output multi-Relief weights' in line:
#            print line
#            results.next()
#            break
#     while line:
#        try:        
#            tmp_line=results.next().split('\t')
#            print tmp_line
#            tmp_line.insert(0,name)
#            del tmp_line[-1]
#            tmp_array = np.array(tmp_line)
#            print 'array = ' + str(tmp_array)
#            data_array = np.vstack((data_array,tmp_array))
#        except StopIteration:
#            break
#     return data_array
#data_array=np.array([name,0,0,0,0,'a', 0, 'b'])
#data_array = run_mh('/tmp/test0_aligned.fasta','test0',data_array) 
#print 'final array =' + str(data_array)
#np.savetxt(data_array,delimiter='\t')
dict = {'DnaA':'/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaA-alignment/Analysis',
        'DnaC':'/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaC-alignment/Analysis',
        'DnaG':'/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaG-alignment/Analysis',
        'DnaB':'/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/DnaB-alignment/Analysis',
        }
with open('/tmp/compiled_trees.txt','a') as outfile:
    for n,d in dict.iteritems():
        files = glob.glob(d+'/*tree.txt')
        for f in files:
            print f
            with open(f,'r') as infile:
                outfile.write(infile.read())
