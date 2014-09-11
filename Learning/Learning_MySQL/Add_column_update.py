# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 16:14:45 2014

@author: pczrr
"""

import MySQLdb as mdb

connection = mdb.connect(host='localhost',db='DnaE_sequences',user='pczrr',passwd='Roble8002~')

cursor = connection.cursor()

#tablelist = ('Tenericutes_sequences')
#
#print tablelist[0]

cursor.execute("SHOW TABLES")
for (table_name,) in cursor:
#        cursor.execute("create index " + table_name + "_OrgID on `DnaE_sequences`.`" 
#        + table_name + "`(Organism_ID)")
        if 'Test' in table_name:
            continue
#        cursor.execute("alter table " + table_name + " add column `Lineage` VARCHAR(100) NULL AFTER `Organism_ID`")       
#        cursor.execute("update " + table_name + " a, Test b set a.Lineage=b.Lineage where a.Organism_ID=b.Organism_ID")
#        print table_name +' updated'        
#        if table_name in tablelist:
#        cursor.execute("alter table " + table_name + " add column `Organism` VARCHAR(200) NULL AFTER `Accession_Number`")        
#        cursor.execute("alter table " + table_name + " add column `Length` VARCHAR(5) NULL AFTER `Organism`")
#        cursor.execute("alter table " + table_name + " add column `Organism_ID` VARCHAR(12) NULL AFTER `Length`")
#        cursor.execute("alter table " + table_name + " add column `Entry_Name` VARCHAR(24) NULL AFTER `Length`")
        cursor.execute("update `" + table_name + "` a, Test b set a.Organism=b.Organism where a.Accession_Number=b.Accession_Number")
        cursor.execute("update `" + table_name + "` a, Test b set a.Length=b.Length where a.Accession_Number=b.Accession_Number")
        cursor.execute("update `" + table_name + "` a, Test b set a.Organism_ID=b.Organism_ID where a.Accession_Number=b.Accession_Number")         
        cursor.execute("update `" + table_name + "` a, Test b set a.Entry_Name=b.Entry_Name where a.Accession_Number=b.Accession_Number")        
        print table_name +' updated'
#        else: 
#            continue
#cursor.execute("update `DnaE_sequences`.`Actinobacteria_sequences` set `Pol-type`=default")
connection.commit()
connection.close()