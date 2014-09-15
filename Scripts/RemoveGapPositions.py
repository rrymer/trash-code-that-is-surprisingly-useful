# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 16:14:45 2014

@author: 
"""

import MySQLdb as mdb
import sys
    
def identify_gap_positions(table,column,ratio,l):
    cursor.execute("select avg(length(`" + column + "`)) from `" + table + "`")
    n=cursor.fetchall()[0]
    n=str(n[0])
    n=float(n)
    cursor.execute("select count(*) from`" + table + "` where `" + column + "` is not Null")
    cutoff=cursor.fetchone()[0]
    cutoff = str(cutoff)
    cutoff = float(cutoff)*ratio
    i=1
    print 'examining alignment for mostly gap positions.'
    while i<n:
        print str(100*i/n) + '% of alignment examined.'
        cursor.execute("select substring(" + column + ", " + str(i) + ",  1), count(*) from `" + table + "` group by substring(" + column + ", " + str(i) + ",  1)")
        results = dict(cursor.fetchall())
        try:        
            count = results['-']
        except KeyError:
                count = 0
        if count <= cutoff:
            l.append(i)
        i = i + 1
    return l

def remove_gap_positions(table,source,dest,source_index,dest_index,positions):
    i=1
    print 'calculating gap-reduced alignment.'    
    for p in positions:
        cursor.execute("update `" + table + "` set `" + dest + "` = concat(`" + dest + "`, substring(`" + source + "`, " + str(p) 
        + ", 1)) where " + source +" is not Null")
        cursor.execute("update `" + table + "` set `" + dest_index + "` = concat(`" + dest_index + "`, ' ', substring_index(substring_index(`" 
        + source_index + "`,' '," + str(p+1) + "),' ',-1)) where " + source +" is not Null")
        print 'calculating gap-reduced alignment, current position is ' + str(p)
        i=i+1
        connection.commit()

def index_alignment(table,algnmt,index,indexing_col):
    cursor.execute("select avg(length(`" + algnmt + "`)) from `" + table + "`")
    n=cursor.fetchall()[0]
    n=str(n[0])
    n=float(n)
    print n
    i=1
    print 'calculating alignment index.'    
    while i<n:        
        sys.stdout.write( 'indexing ' + str(100*i/n) + '% complete')
        cursor.execute("update `" + table + "` set `" + index + "` = if(substring("+algnmt+","+str(i)+",1) not like '-',concat("+
        index+",' ',"+indexing_col+"),concat("+index+",' ','-'))")
        cursor.execute("update `" + table + "` set `" + indexing_col + "` = if(substring("+algnmt+","+str(i)+",1) not like '-',"
        +indexing_col+"+1,"+indexing_col+")")
        i=i+1
        connection.commit()

def gap_free_coords(table,gfalgnmt,index,coords):
    cursor.execute("select avg(length(`" + gfalgnmt + "`)) from `" + table + "`")
    n=cursor.fetchall()[0]
    n=str(n[0])
    n=float(n)
    i=1
    print 'calculating gap-reduced alignment coordinates.'      
    while i<n:
        print 'coordinate calculation ' + str(100*i/n) + '% complete'
        cursor.execute("update `" + table + "` set `" + coords + "` = if(substring("+gfalgnmt+","+str(i)+
        ",1) not like '-',concat("+coords+",' ',substring("+gfalgnmt+","+str(i)+",1),',',substring_index(substring_index("
        +index+",' ',"+str(i)+"),' ',-1),',',"+str(i)+"),"+coords+")")
        i=i+1
        connection.commit()

connection = mdb.connect(host='localhost',db='FamilyCpolymerases',user='sequser')
cursor = connection.cursor()
#index_alignment('DnaGs','Aligned_seq','Aligned_seq_index','Indexing')
l=[]
l = identify_gap_positions('DnaGs','Aligned_seq',0.9,l)
remove_gap_positions('DnaGs','Aligned_seq','gfAligned_seq','Aligned_seq_index','gfAligned_seq_index',l)
gap_free_coords('DnaGs','gfAligned_seq','gfAligned_seq_index','gfAligned_seq_coords')
connection.close()




#cursor.execute("update `DnaE_sequences`.`Actinobacteria_sequences` set `Pol-type`=defaulcall
