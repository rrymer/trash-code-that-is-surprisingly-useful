# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 16:14:45 2014

@author: pczrr
"""

import MySQLdb as mdb
import subprocess as sp
import glob
import sys
import os
from __main__ import logger

def format_algnmt(algnmt,inform,outext):
    com = "convalign -i {} {} {}".format(inform,outext,algnmt)
    logger.debug('convert alignment command: {}'.format(com))
    p = sp.Popen([com],stderr=sys.stderr,stdout=sys.stdout)
    p.wait()
    algnmt = glob.glob(os.path.split(algnmt)[0] + '*.' + outext)
    if len(algnmt):
        logger.info('alignment conversion successful')
        return algnmt
    else:
        logger.error('conversion failed')
        return
    
def upload(temp_t,dest_t,connection,algnmt,algnmt_col,field_sep='\t',line_sep=None):
    cursor = connection.cursor()
    check_sql="select Accession_Number,'' from {} where {} is null"
    cursor.execute(check_sql.format(dest_t))
    rows=dict(cursor.fetchall())
    cnt0 = []
    for k,v in rows.iteritems():
        cnt0.append(k)
    if line_sep:
        sql = "load data local infile '{}' ignore into table {} fields terminated by {} {} (Header,{})"
        logger.debug('load alignment data statement: {}'.format(sql.format(algnmt,temp_t,field_sep,line_sep,algnmt_col)))
        cursor.execute(sql.format(algnmt,temp_t,field_sep,line_sep))
    else:
        sql = "load data local infile '{}' ignore into table {} fields terminated by {} (Header,{})"
        logger.debug('load alignment data statement: {}'.format(sql.format(algnmt,temp_t,field_sep,algnmt_col)))
        cursor.execute(sql.format(algnmt,temp_t,field_sep))
    connection.commit()
    sql = "update {} a, {} b set a.{}=b.{} where a.Accession_Number=b.Accession_Number"
    logger.debug('update aligned seqs to table statement: {}'.format(sql.format(dest_t,temp_t,algnmt_col,algnmt_col)))
    cursor.execute(sql.format(dest_t,temp_t))
    connection.commit()
    cursor.execute(check_sql.format(dest_t))
    rows=dict(cursor.fetchall())
    cnt1 = []
    for k,v in rows.iteritems():
        cnt1.append(k)
    updated = len(cnt1) - len (cnt0)
    if 0 >= updated:
        logger.error('alignment upload failed.')
        return
    else:
        logger.info('{} aligned sequences uploaded into table {}'.format(updated,dest_t))
        cursor.execute("truncate {}".format(temp_t))
        connection.commit()

def identify_gap_positions(table,column,ratio,l):
    sql="select avg(length(`{}`)) from `{}`"
    logger.debug('alignment length query: {}'.format(sql.format(column,table)))
    cursor.execute(sql.format(column,table))
#    cursor.execute("select avg(length(`" + column + "`)) from `" + table + "`")
    n=cursor.fetchall()[0]
    n=str(n[0])
    n=float(n)
    sql="select count(*) from `{}` where `{}` is not null"
    logger.debug('row count sql query: {}'.format(sql.format(table,column)))
    cursor.execute(sql.format(table,column))
#    cursor.execute("select count(*) from`" + table + "` where `" + column + "` is not Null")
    cutoff=cursor.fetchone()[0]
    cutoff = str(cutoff)
    cutoff = float(cutoff)*ratio
    i=1
    logger.info('examining alignment in table {} for mostly gap positions.'.format(table))
    sql="select substring({},{},1) count(*) from `{}` group by substring({},{},1)"
    logger.debug('gap character count statement: {}'.format(sql.format(column,str(i),table,column,str(i))))
    while i<n:
        print str(100*i/n) + '% of alignment examined.'
#        cursor.execute("select substring(" + column + ", " + str(i) + ",  1), count(*) from `" + table + "` group by substring(" + column 
#        + ", " + str(i) + ",  1)")
        cursor.execute(sql.format(column,str(i),table,column,str(i)))        
        results = dict(cursor.fetchall())
        try:
            count = results['-']
        except KeyError:
                count = 0
        if count <= cutoff:
            l.append(i)
        i = i + 1
    return l

def index_alignment(connection,table,algnmt,index,indexing_col):
    cursor=connection.cursor
    sql="select avg(length({})) from {}"
    logger.debug('select alignment length sql query: {}'.format(sql.format(algnmt,table)))
    cursor.execute(sql.format(algnmt,table))
#    cursor.execute("select avg(length(`" + algnmt + "`)) from `" + table + "`")
    n=cursor.fetchall()[0]
    n=str(n[0])
    n=float(n)
    logger.info('alignment total length: {}'.format(str(n)))
    i=1
    print 'calculating alignment index.'
    sql1="update {} set {} = if(substring({},{},1) not like '-',concat({},' ',{}),concat({},' ','-'))"
    sql2="update {} set {}=if(substring({},{},1) not like '-',{}+1,{})"
    logger.debug=('update index sql statement'.format(sql1.format(table,index,algnmt,str(i),index,indexing_col,index)))
    logger.debug=('update indexing_col sql statement'.format(sql2.format(table,indexing_col,algnmt,str(i),indexing_col,indexing_col)))
    while i<n:        
        sys.stdout.write( 'indexing ' + str(100*i/n) + '% complete')
        cursor.execute(sql1.format(table,index,algnmt,str(i),index,indexing_col,index))
#        cursor.execute("update `" + table + "` set `" + index + "` = if(substring("+algnmt+","+str(i)+",1) not like '-',concat("+
#        index+",' ',"+indexing_col+"),concat("+index+",' ','-'))")
        cursor.execute(sql2.format(table,indexing_col,algnmt,str(i),indexing_col,indexing_col))
#        cursor.execute("update `" + table + "` set `" + indexing_col + "` = if(substring("+algnmt+","+str(i)+",1) not like '-',"
#        +indexing_col+"+1,"+indexing_col+")")
        i=i+1
        connection.commit()
    check_sql="select max(length{})"
    cursor.execute(check_sql.format(index))
    check_results = cursor.fetchall()[0]
    logger.info('alignment indexing complete for table {}. {} positions indexed for an alignment {} characters long'
        .format(table,check_results,str(n)))
    

def remove_gap_positions(connection,table,source,dest,source_index,dest_index,positions):
    i=1
    logger.info('calculating gap-reduced alignment for table {}.'.format(table))
    sql1="update {} set {} = concat({},substring({},{},1) where {} is not null)"
    sql2="update {} set {} = concat({},' ',substring_index(substring_index({},' ',{}),' ',-1) where {} is not null)"
    logger.debug('update gap-reduced alignment sql statement: {}'.format(sql1.format(table,dest,dest,source,str(positions[0]),source)))
    logger.debug('update gap-reduced alignment index statement: {}'
        .format(sql2.format(table,dest_index,dest_index,source_index,str(positions[0]+1),source)))
    cursor=connection.cursor()
    logger.info('calculating gap-reduced alignment for table {}, {} positions to be removed'.format(table,str(len(positions))))
    for p in positions:
        cursor.execute(sql1.format(sql1.format(table,dest,dest,source,str(p),source)))
#        cursor.execute("update `" + table + "` set `" + dest + "` = concat(`" + dest + "`, substring(`" + source + "`, " + str(p) 
#        + ", 1)) where " + source +" is not Null")
        cursor.execute(sql2.format(table,dest_index,dest_index,source_index,str(p+1),source))
#        cursor.execute("update `" + table + "` set `" + dest_index + "` = concat(`" + dest_index + "`, ' ', substring_index(substring_index(`" 
#        + source_index + "`,' '," + str(p+1) + "),' ',-1)) where " + source +" is not Null")
        print 'calculating gap-reduced alignment, current position is ' + str(p)
        i=i+1
        connection.commit()
    check_sql = "select avg(length({})),avg(length({})) from {} where {} is not null"
    logger.debug('check sql query: {}'.format(source,dest,table,source))
    cursor.execute(check_sql.format(dest,source,table,source))
    check_results=dict(cursor.fetchall())
    for k,v in check_results.iteritems():
        logger.info('finished calculating gap-reduced alignment for table {}. Removed {} positions.'.format(table,str(float(k)-float(v))))
    return

def coords(connection,table,algnmt,index,coords):
    cursor=connection.cursor
    logger.info('calculating alignment coordinates for {} in table {}'.format(algnmt,table))
    sql="select avg(length({})) from {}"
    logger.debug('calculate alignment length sql query:{}'.format(sql.format(algnmt,table)))
    cursor.execute(sql.format(algnmt,table))
#    cursor.execute("select avg(length(`" + algnmt + "`)) from `" + table + "`")
    n=cursor.fetchall()[0]
    n=str(n[0])
    n=float(n)
    i=1
    sql="update {} set {} = if(substring({},{},1) not like '-',concat({},' ',substring({},{},1),',',substring_index(substring_index({},' ',{}),' ',-1),',',{}),{})"
    logger.debug('update coords statement for table {}:{}'
    .format(table,sql.format(table,coords,algnmt,str(i),coords,algnmt,str(i),index,str(i),str(i),coords)))    
    logger.info('calculating alignment coordinates for table {}'.format(table))      
    while i<n:
        print 'coordinate calculation ' + str(100*i/n) + '% complete'
        cursor.execute(sql.format(table,coords,algnmt,str(i),coords,algnmt,str(i),index,str(i),str(i),coords))
#        cursor.execute("update `" + table + "` set `" + coords + "` = if(substring("+algnmt+","+str(i)+
#        ",1) not like '-',concat("+coords+",' ',substring("+algnmt+","+str(i)+",1),',',substring_index(substring_index("
#        +index+",' ',"+str(i)+"),' ',-1),',',"+str(i)+"),"+coords+")")
        i=i+1
        connection.commit()
if __name__ == '__main__':
    
    algnmt = format_algnmt(algnmt,inform,outext)
    upload(temp_t,dest_t,connection,algnmt,field_sep='\t',line_sep=None,algnmt_col)
    identify_gap_positions(table,column,ratio,l)
    index_alignment(connection,table,algnmt,index,indexing_col)
    remove_gap_positions(connection,table,source,dest,source_index,dest_index,positions)
    coords(connection,table,algnmt,index,coords)

#format_algnmt
#connection = mdb.connect(host='localhost',db='FamilyCpolymerases',user='sequser')
#cursor = connection.cursor()
#index_alignment('DnaGs','Aligned_seq','Aligned_seq_index','Indexing')
#l=[]
#l = identify_gap_positions('DnaGs','Aligned_seq',0.9,l)
#remove_gap_positions('DnaGs','Aligned_seq','gfAligned_seq','Aligned_seq_index','gfAligned_seq_index',l)
#coords('DnaGs','gfAligned_seq','gfAligned_seq_index','gfAligned_seq_coords')
#connection.close()




#cursor.execute("update `DnaE_sequences`.`Actinobacteria_sequences` set `Pol-type`=defaulcall