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
    cursor.execute("delete from " + table_name + " where isnull(Lineage)")
#cursor.execute("update `DnaE_sequences`.`Actinobacteria_sequences` set `Pol-type`=default")
connection.commit()
connection.close()