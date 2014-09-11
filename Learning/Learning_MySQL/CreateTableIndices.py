# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 16:14:45 2014

@author: pczrr
"""

import MySQLdb as mdb

connection = mdb.connect(host='localhost',db='DnaE_sequences',user='pczrr',passwd='Roble8002~')

cursor = connection.cursor()

cursor.execute("SHOW TABLES")
for (table_name,) in cursor:
        print table_name
        cursor.execute("create index " + table_name + "_Header on `DnaE_sequences`.`" 
        + table_name + "`(Header)")
#cursor.execute("update `DnaE_sequences`.`Actinobacteria_sequences` set `Pol-type`=default")
connection.close()