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
        if 'PolC_sequences' in table_name:
            continue
        if 'Test' in table_name:
            continue
        cursor.execute("update `" 
        + table_name + "` a, `PolC_sequences` b set a.`Pol-type`='PolC' where a.`Header` = b.`Header`")
        print table_name +'updated'
#cursor.execute("update `DnaE_sequences`.`Actinobacteria_sequences` set `Pol-type`=default")
connection.close()