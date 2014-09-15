# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 16:14:45 2014

@author: 
"""

import MySQLdb as mdb

connection = mdb.connect(host='localhost',db='DnaE_sequences',user='pczrr',passwd='Roble8002~')

cursor = connection.cursor()

#tablelist = ('Tenericutes_sequences')
#
#print tablelist[0]

phyla_taxid_dict = {
    'Actinobacteria' : '201174',
    'Bacteroidetes' : '68336',
    'Chlamydiae' : '51290',
    'Cyanobacteria' : '1117',
    'Firmicutes' : '1239',
    'Fusobacteria' : '32066',
    'Proteobacteria' : '1224',
    'Spirochaetes' : '203691',
    'Tenericutes' : '544448',
    'Thermotogae' : '200918',
    'Thermodesulfobacteria' : '200940',
    'Caldiserica' : '67814',
    'Chloroflexi' : '200795',
    'Chrysiogenetes' : '200938',
    'Aquificae' : '200783',
    'Armatimonadetes' : '67819',
    'Deferribacteres' : '200930',
    'Deinococcus-Thermus' : '1297',
    'Dictyoglomi' : '68297',
    'Elusimicrobia' : '74152',
    'Fibrobacteres/Acidobacteria' : '131550',
    'Gemmatimonadetes' : '142182',
    'Nitrospinae' : '1293497',
    'Nitrospirae' : '40117',
    'Planctomycetes' : '203682',
    'Synergistetes' : '508458',
    'Unclassified' : '2323',
    'environmental samples' : '48479'
    }

cursor.execute("SHOW TABLES")
for (table_name,) in cursor:
#        cursor.execute("create index " + table_name + "_OrgID on `DnaE_sequences`.`" 
#        + table_name + "`(Organism_ID)")
        if 'All' not in table_name:
            continue
        cursor.execute("alter table " + table_name + " add column `Phylum` VARCHAR(50) NULL AFTER `Lineage`")       
        for k, v in phyla_taxid_dict.iteritems():
            print 'search term: %' + v + ' 2%'
            cursor.execute("update " + table_name + " a set a.Phylum='" + k + "' where a.Lineage like '%" + v + " 2%'" )
            print k + ' members flagged in ' + table_name
        print table_name +' updated'        
#        if table_name in tablelist:
#            cursor.execute("alter table " + table_name + " add column `Organism` VARCHAR(200) NULL AFTER `Accession_Number`")        
#            cursor.execute("alter table " + table_name + " add column `Length` VARCHAR(5) NULL AFTER `Organism`")
#            cursor.execute("alter table " + table_name + " add column `Organism_ID` VARCHAR(6) NULL AFTER `Length`")       
#            cursor.execute("update `" + table_name + "` a, Test b set a.Organism=b.Organism where a.Accession_Number=b.Accession_Number")
#            cursor.execute("update `" + table_name + "` a, Test b set a.Length=b.Length where a.Accession_Number=b.Accession_Number")
#            cursor.execute("update `" + table_name + "` a, Test b set a.Organism_ID=b.Organism_ID where a.Accession_Number=b.Accession_Number")         
#            print table_name +' updated'
#        else: 
#            continue
#cursor.execute("update `DnaE_sequences`.`Actinobacteria_sequences` set `Pol-type`=default")
connection.commit()
connection.close()
