# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 16:21:47 2014

@author: rur
"""

import MySQLdb as mdb
import glob
import subprocess
import os
import multiprocessing
from Bio.Align.Applications import MafftCommandline
import itertools
import logging
import time
#import fileinput

###functions
class Logger():
    logger=None
    def myLogger(self,path,name,level):
        print 'initializing logger {} located at {}'.format(name,path)
        if None == self.logger:
            self.logger=logging.getLogger(name)
            self.logger.setLevel(level)
            self.handler=logging.FileHandler('{}align_and_tree_{}.log'.format(path,name))
            formatter=logging.Formatter("%(message)s")
            self.handler.setFormatter(formatter)
            self.logger.addHandler(self.handler)
        return self.logger

def reinitialize_logging(path):
    reload(logging)
    main_loggers = Logger()
    main_logger = main_loggers.myLogger(basedir,'main',logging.INFO)
    return main_logger

def connect_to_mysqdb(host, db, un):
    connection = mdb.connect(host=host,db=db,user=un)
    return connection

def worker(in_queue):
    item = in_queue.get()
    MakeTrees(item)

def find_groups(fnclogger,table,group_field,query=''):
    connection = connect_to_mysqdb('localhost', 'FamilyCpolymerases', 'sequser')
    cursor=connection.cursor()
    query = 'where {}'.format(query)
    main_logger.info("searching table {} for a list of {}s.".format(table,group_field))
    sql="select {},count(*) from {} {} group by {}"
    fnclogger.debug=("determine counts sql query:{}".format(sql.format(group_field,table,query,group_field)))
    cursor.execute(sql.format(group_field,table,query,group_field))
    groups=dict(cursor.fetchall())
    main_logger.info("groups found in table {}:{}.".format(table,str(groups)))
    connection.close()
    return groups

def ref_dexport (fnclogger,table,group_field,groups,query):
    connection = connect_to_mysqdb('localhost', 'FamilyCpolymerases', 'sequser')
    cursor = connection.cursor()
    if query:
        query = 'and {}'.format(query)
    main_logger.info('exporting reference data')
    hsql="select concat('Group:Reference', '|', '{}', '|',Accession_Number), {} from {} where {} like '{}' {} {}" 
    lsql="order by rand() limit 10 into outfile '/tmp/{}_Reference_data.fasta' fields terminated by '\n' lines starting by '>'"
    for g,c in groups.iteritems():
        fnclogger.info("exporting reference data for group {}".format(group_field))
        if os.path.isfile('/tmp/' + g + '_Reference_data.fasta'):
            fnclogger.error("reference data for {} {} data exists already".format(group_field,g))
            break
        else:
           i=0
           active = g
           for g in groups:
               if g in active:
                   continue
               else:
                   formatted_sql=hsql.format(group_field,seq_field,table, group_field,g,query,lsql
                       .format(active+table+str(i).zfill(3)))
                   print 'exporting reference file:{}'.format(active+table+str(i).zfill(3))
                   fnclogger.info("group selection sql query:\n {}".format(formatted_sql))
                   try:
                       cursor.execute(hsql.format(group_field,seq_field,table, group_field,g,query,lsql
                           .format(active+table+str(i).zfill(3))))
                   except mdb.OperationalError:
                       if os.path.isfile('/tmp/{}_Reference_data.fasta'.format((active+table+str(i).zfill(3)))):
                           i=i+1
                           cursor.execute(hsql.format(group_field,seq_field,table, group_field,g,query,lsql
                           .format(active+table+str(i).zfill(3))))
                   fnclogger.info("assmebling reference file for {} {}".format(group_field,g))
           try:
               files = glob.glob('/tmp/' + active + table + '*' + '_Reference_data.fasta')
               with open('/tmp/' + active + '_' + table + '_Reference_data.fasta','a') as outFile:
                   for f in files:
                       with open(f,'r') as inFile:
                           outFile.write(inFile.read())
           except IOError:
               fnclogger.error("unable to assemble files for {} {}".format(group_field,active))
               continue
    connection.close()
    return
        
def seq_dexport (fnclogger,table,group_field,groups,test_field,test_grp,query):
    connection = connect_to_mysqdb('localhost', 'FamilyCpolymerases', 'sequser')
    cursor = connection.cursor()
    main_logger.info("exporting primary data for table {}".format(table))
    query = 'and {}'.format(query)    
    hsql="select concat('Group:{}', '|', '{}','|',Accession_Number), {} from {} where {}='{}' {} {}"
    lsql="order by rand() limit 300 into outfile '/tmp/{}{}{}.fasta' fields terminated by '\n' lines starting by '>';"
    fnclogger.info("select group data statement: {}".format(hsql
    .format('::group::','tst_grp',seq_field,table,group_field,'::group::',query,lsql.format('::group::',table,seq_field))))
    search=[]
    print groups
    for k,v in groups.iteritems():
        if int(v) >= 3:
            print k
            print v
            cursor.execute(hsql.format(k,test_grp,'count(*)',table,group_field,k,query,'group by {}'.format(control_field)))
            print hsql.format(k,test_grp,'count(*)',table,group_field,k,query,'')
            rslts=cursor.fetchall()
            print 'here are the results for {} {}'.format(k,str(rslts))
            try: 
                if int(rslts[0][1]) >= 3:
                    print rslts[0]
                    search.append(k)
                else:
                    fnclogger.info("subgroup {} {} {} is too small to analyze with only {} members".format(k,rslts,table,rslts[1]))
                    continue
            except IndexError, e:
                fnclogger.info("group {} {} is too small to analyze with only {} members".format(k,table,str(v)+str(e)))
                continue
#            search[k]=test_grp
        else:
            fnclogger.info("group {} {} is too small to analyze with only {} members".format(k,table,v))
            continue
    print 'search list =' + str(search)
    for grp in search:
            fnclogger.info("exporting {} data for {} {} {} {} {}".format(seq_field,group_field,grp,test_field,test_grp,table))
            filenames['/tmp/{}{}{}.fasta'.format(grp+table,test_field+test_grp,seq_field)]=grp
#    #        if os.path.isfile('/tmp/{}{}.fasta'.format(v+table,seq_field)):
#    #            print 'file exists for {} {}'.format(v,table)
#    #            raw_input('is file present?')
#    #            subprocess.Popen("echo 'Roble8002~' | sudo -S rm '/tmp/{}{}.fasta'".format(v+table,seq_field),shell=True)
#            if os.path.isfile('/tmp/' + grp + '_' + table + '_Reference_data.fasta'):      
#                try:
            cursor.execute(hsql.format(grp,test_grp,seq_field,table,group_field,grp,query,lsql.format(grp+table,test_field+test_grp,seq_field)))
#                except mdb.OperationalError, e:
#                    print 'export error' 
#                    if os.path.isfile('/tmp/{}{}{}.fasta'.format(grp+table,test_field+test_grp,seq_field)): 
#                        print 'attempting to recover for {} {}'.format(table,grp)
#                        fnclogger.error("{} {} data file appears to exist, {}".format(grp+table,test_field+test_grp,e))
#                        print 'attempting to recover for {}'.format(table,grp)
#                        raw_input('is file present?  If so, remove it.')
#                        cursor.execute(hsql.format(grp,seq_field,table,group_field,grp,query,lsql.format(grp+table,test_field+test_grp,seq_field)))
    #                    pass
    #                else:
    #                    print 'export is not working for some other reason: {}'.format(e)
    #                    fnclogger.error("export of data file for group {} was not successful with error {}, skipping".format(v,e))
    #                    return
#                    if os.path.isfile('/tmp/{}{}{}.fasta'.format(grp+table,test_field+test_grp,seq_field)): 
#    print filenames
#    fnclogger.info("assmebling data file for table {} and {} {}".format(table,group_field+grp,test_field+test_grp))
#    files = glob.glob('/tmp/{}{}{}.fasta'.format('*'+table,'*',seq_field))
#    for f in files:

    #                    else:
    #                        fnclogger.info('data for {} {} did not export, aborting.'.format(grp,table))
#    #                        return
#                    except IOError:
#                        print 'stuff'
#                else:
#                    fnclogger.error("no reference data for group {}, skipping.".format(grp+table+test_field+test_grp))            
#                    connection.close()            
#                    return
    connection.close()
    return hsql,filenames
"""
This is a cool idea, but hard to implement
def select_seq(table,refIDs,groupby,**queries):
    connection = connect_to_mysqdb('localhost', 'FamilyCpolymerases', 'sequser')
    cursor = connection.cursor()
    results_dict={}
    for ID in refIDs:
        logger.info("sql query for reference sequence:\n{}".format("select {}, {} from {} where {} = '{}'"
        .format(ID_field,seq_field,table,ID_field,refID)))
        cursor.execute("select {}, {} from {} where {} = '{}'".format(ID_field,seq_field,table,ID_field,refID))
        ref_seqs=dict(cursor.fetchall())
        results_dict[ID]=ref_seqs
        logger.info('executing argument queries: {}'.format(str(queries)))
    for nm,q in queries:
        logger.info("sql query for sample sequences:\n{}".format("select {}, {} from {} {} {}"
        .format(ID_field,seq_field,table,q,groupby)))
        cursor.execute("select {}, {} from {} {} {}".format(ID_field,seq_field,table,q,groupby))
        results=dict(cursor.fetchall())
        results_dict[nm]=results
    connection.close()
    return ref_seqs,results_dict

def sql_constructor(table,qdict):
    sql = "select * from ({})"
    subsql="{}"
    subgrpsql="{}"
    grpsqls={}
    i=0
    for nm,rslts in qdict.iteritems():
        for ID,x in rslts.iteritems():
            qxsql = "select '{}', {} where {} = '{}'".format(nm.format(ID),s v eq_field,ID_field,ID)
            subsql = subsql.format(qxsql)
        subgrpsql=subgrpsql.format(subsql)d
    grpsqls[grps[i]]=subsql
    for qID,sql in grpsqls.iteritems():
        sql = sql.format("{} = '{}'".format(ID_field,refIDs[table]))
        main_logger.info('final sql query for data set {}:{}'.format(nm,sql))
    return fasta_export(grpsqls)

def fasta_export (grp,seq_dict):
    with open(workingdir+'/Data/{}'.format(grp + '_seqs.txt'),'a') as outfile:
        for nm,rslts in seq_dict.iteritems():
            for ID,seq in rslts:
                outfile.write('>{}\n{}'.format(nm.format(ID),seq))
    expsql="{} into outfile '/tmp/{}.fasta' fields terminated by '\n' lines starting by '>'"
    for nm,sql in sql_dict:
        logger.info("sql statement for {}:{}".format(nm,expsql.format(sql,nm)))
        cursor.execute(expsql.format(sql,nm))
    connection.close()
"""

def MakeAlignments(seqs,name,path):   ##aligns exported data 
    if os.path.isfile(path + name + '_aligned.txt') is False:
        in_file = seqs
        mafft_cline = MafftCommandline(input=in_file, auto=True, reorder=True)
        stdout, stderr = mafft_cline()
        handle = open(path + name + '_aligned.txt', 'w')
        handle.write(stdout)
        handle.close()  
#    subprocess.Popen(['mafft ' + seqs + ' > ' + outputdir +  name + '_aligned.txt'],shell=True,stdout=log)
    
def MakeTrees(algnt):      ##makes trees          
    p = subprocess.Popen(['phyml', '-i', algnt, '-d', 'aa','-q','--no_memory_check','--quiet'])
    p.wait()
    
def AssembleTreeFile(trees): ##assembles complete tree file
    with open(basedir+'/scratch/' + 'compiledtrees.txt', 'w') as outfile:     
        for t in trees:
            if os.path.getsize(t) <= 0:
                continue
            print 'appending ' + os.path.splitext(os.path.split(t)[1])[0] + ' to compiled tree file.'
            with open(t) as infile:        
                outfile.write(infile.read())
"""
    what are we selecting for?
        field values in the db
            How many?
                at most two, else the samples would be too small
    What parameters do we need to do so?
        which fields, the target values, etc.
            and those are?
                well, I would like it be general, but specifically phylum and replicative polymerase components profile
    What are we going to do with the data?
        we are going to compare them against each other?
            how?
                using a phylogenetic tree, multiharmony, and hmm-hmm comparison
    What does the program need to know to do so?
        database
        table
        where to put the data
        how to pick it back up
        how to select the data
"""
def process(fnclogger,table,ref_query,filenames):
    fnclogger.info("reference sequence sql query:{}".format(ref_query))
    control_groups = find_groups(fnclogger,table,control_field,query=ref_query)
    test_groups = find_groups(fnclogger,table,test_field,query=ref_query)
    print type(test_groups)
    print type(table)
    print type(test_field)
    print "{} groups found in table {}:{}".format(test_field,table,str(test_groups))
    fnclogger.info("{} groups found in table {}:{}".format(test_field,table,str(test_groups)))
    fnclogger.info("{} groups found in table {}:{}".format(control_field,table,str(control_groups)))
    ref_dexport (fnclogger,table,control_field,control_groups,ref_query)   
    for grp,cnt in test_groups.iteritems():
        main_logger.info("exporting sequences for {} group {}".format(test_field,grp))
        test_query="{} and {} = '{}'".format(ref_query,test_field,grp)
        hsql,filenames = seq_dexport(fnclogger,table,control_field,control_groups,test_field,grp,test_query)
        for f,grp in filenames.iteritems():
            with open(f,'a') as outFile:
                with open('/tmp/' + grp + '_' + table + '_Reference_data.fasta','r+') as inFile:
                    outFile.write(inFile.read())
                if refID:
                    connection = connect_to_mysqdb('localhost', 'FamilyCpolymerases', 'sequser')
                    cursor = connection.cursor()
#                    fnclogger.info("select reference sequence sql query: {}".format(hsql.format('Reference',table,seq_field,ID_field,refID,'','')))
                    cursor.execute(hsql.format('Reference','uref',seq_field,table,ID_field,refID,'',''))
                    rslts = dict(cursor.fetchall())
                    outFile.write('> {} \n{}'.format('Group:Reference|uref|{}'.format(refID),rslts['Group:Reference|uref|{}'.format(refID)]))
                    connection.close()
        

if __name__=='__main__':
##parameters and definitions
    basedir='/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/'
    DnaA_loggers=None
    DnaB_loggers=None
    DnaCI_loggers=None
    DnaG_loggers=None
    DnaA_logger=None
    DnaB_logger=None
    DnaCI_logger=None
    DnaG_logger=None
    hsql=None
    lsql=None
    table_loggers = {'DnaA':DnaA_loggers,'DnaB':DnaB_loggers,'DnaC':DnaCI_loggers,'DnaG':DnaG_loggers}
    logger_dict = {'DnaA':DnaA_logger,'DnaB':DnaB_logger,'DnaC':DnaCI_logger,'DnaG':DnaG_logger}
    control_field='Phylum'
    test_field='PolProfile'
    tables={'DnaA':'DnaAs','DnaB':'DnaBs','DnaC':'DnaCIs','DnaG':'DnaGs'}
    refIDs={'DnaG':'P0ABS5','DnaC':'P0AEF0','DnaD':'P39787','DnaA':'P03004','DnaB':'P0ACB0'}
    ID_field='Accession_Number'
    seq_field='Sequence'
    phyla=['Acidobacteria','Actinobacteria','Aquificae','Bacteroidetes','Caldiserica','Chlamydiae',
    'Chlorobi','Chloroflexi','Chrysiogenetes','Cyanobacteria','Deferribacteres','Deinococcus-Thermus','Dictyoglomi','Elusimicrobia',
    'Fibrobacteres','Firmicutes','Fusobacteria','Gemmatimonadetes','Ignavibacteria','Nitrospirae','Planctomycetes','Proteobacteria',
    'Spirochaetes','Synergistetes','Tenericutes','Thermodesulfobacteria','Thermotogae','Verrucomicrobia']
##initialize logging
    main_logger = reinitialize_logging(basedir)    
##find and assess groups
    main_logger.info("BEGIN SEQUENCE SELECTION AND EXPORT")
    p0=multiprocessing.Pool(8)
    for k,v in tables.iteritems():
        filenames={}
        main_logger = reinitialize_logging(basedir) 
        table = v
        refID=refIDs[k]
        ref_query="PolGroup='ref{}'".format(str(k))
        workingdir="/Users/pczrr/Documents/Work/Project-Folders/B-subtilis-DNA-Replication/Processing/{}-alignment/".format(k)    
        table_loggers[k] = Logger()        
        logger_dict[k] = table_loggers[k].myLogger(workingdir,k,logging.DEBUG)
        logger_dict[k].info('logger initialized for {}'.format(k))
        process(logger_dict[k],table,ref_query,filenames)
    p0.close()
    p0.join()
    main_logger = reinitialize_logging(basedir) 
    files = glob.glob('/tmp/*Sequence.fasta')    
    p1 = multiprocessing.Pool(8)
    if files:
        main_logger.info('data export completed')
    else:
        main_logger.error('data export was not successful')
    main_logger.info("BEGIN SEQUENCE ALIGNMENT")
    for f in files:
        main_logger.info('aligning file {}'.format(f))
        name = os.path.splitext(os.path.split(f)[1])[0]                    
        p1.apply_async(MakeAlignments, args=(f,name,basedir+'/scratch/'))
    p1.close()
    p1.join()
    
    
##wait for all alignments to finish, then move on to making trees, after a little processing        
    algnts = glob.glob(basedir+'scratch/' + '*_aligned.txt')
    if algnts:
        main_logger.info("alignment complete")
    else:
        main_logger.error('sequence alignment was not successful')
    for a in algnts:
        main_logger.info('converting file {}'.format(a))
        name = os.path.splitext(os.path.split(a)[1])[0]
        print 'post-processing file ' + name
        p4 = subprocess.Popen(["sed 's/Group.*\|//' <" + a + ">"+basedir+"scratch/"+name+".fasta"],shell=True)
        p4.wait()
        p2 = subprocess.Popen(['perl ~/Google\ Drive/Coding/Scripts/Fasta2Phylip.pl ' +
            basedir + 'scratch/' + name + '.fasta ' + basedir + 'scratch/' + name + '.phy'],shell=True)    
        p2.wait()
    p3 = multiprocessing.Pool(8)
    algnts = glob.glob(basedir+'scratch/*.phy')    
#    name = os.path.splitext(os.path.split(a)[1])[0]  
    main_logger.info("BEGIN TREE CONSTRUCTION")      
    iters = itertools.chain(algnts, (None,)*8)
    for a in enumerate(iters):
        print a[1]   
        p3.apply_async(MakeTrees,args=(a[1],))
    p3.close()
    p3.join()
##assemble trees into one file
    
    trees = glob.glob(basedir+'/scratch/' + '*phyml_tree.txt')
    if trees:
        main_logger.info('tree construction complete')
    else:
        main_logger.error('tree construction was not successful')
    main_logger.info("BEGIN TREE COMPILATION")
    AssembleTreeFile(trees)