# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 16:14:45 2014

@author: pczrr
"""

import MySQLdb as mdb

connection = mdb.connect(host='localhost',db='DnaE_sequences',user='pczrr',passwd='Roble8002~')

cursor = connection.cursor()

#seqstorem=('A9EJ43', 'A9G881', 'B0QW19', 'B5IYL8', 'B5JBG6', 'B5K3T6', 'C1IB60', 'C3RQQ8', 'C4FWP2', 'C4G2F9', 'C7XZ93', 'D0CIH6', 'D1RZG0', 'D5QSH0', 'D5QT76', 'D6HLV2', 'D6KTH9', 'D6KXC0', 'E0HWE0', 'E4M170', 'E4M5Y1', 'E4MMZ5', 'E5BT46', 'E8L0C9', 'E8L0G6', 'F0DM47', 'F3A8R6', 'F7Q341', 'F7Q5E1', 'F9QQ41', 'F9QS49', 'F9U0J6', 'G4D7A6', 'G4DJ35', 'G4DLZ8', 'G4DN53', 'G4EIG3', 'G4FWJ7', 'G4FXZ7', 'G4FZ98', 'G4IQR3', 'G4ITL4', 'G4IWL7', 'G4J5T8', 'G4JT48', 'G4K078', 'G4K0K4', 'G6G158', 'G6GKA7', 'G6H5Z6', 'G6HN85', 'G6I0X3', 'G6I737', 'G6IHK4', 'G9X8X2', 'H1I3H0', 'H1IH66', 'H1IMD6', 'H1IQ50', 'H1JCH5', 'H1K161', 'H1K2K4', 'H1M6R3', 'H1MCQ4', 'H1N3Z5', 'H1NJS7', 'H1NLW9', 'H1NZ87', 'H1P3V9', 'H1TVI8', 'H5RJH5', 'H5RKS1', 'H5RZ83', 'H7DUK2', 'I0BE80', 'I0XX78', 'I0XZC3', 'I0YE70', 'I0YEJ7', 'I0YG90', 'Q1VUJ1', 'Q1ZFQ9')

cursor.execute("SHOW TABLES")
with open('/tmp/NullIDs.txt', 'w') as outfile:
    for (table_name,) in cursor:
        if 'Test' in table_name:
            continue
        cursor.execute("select Accession_Number,Organism_ID from " + table_name + " where isnull(Organism_ID)" +
                        "into outfile '/tmp/" + table_name + "_NullIDs.txt'" + 
                        "fields terminated by '\t'")
        with open('/tmp/' + table_name + '_NullIDs.txt') as infile:
            outfile.write(infile.read())
    
   #cursor.execute("update `DnaE_sequences`.`Actinobacteria_sequences` set `Pol-type`=default")
connection.commit()
connection.close()