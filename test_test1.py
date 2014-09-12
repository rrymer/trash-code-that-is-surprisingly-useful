# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 15:12:50 2014

@author: pczrr
"""

from twisted.python.filepath import FilePath
import os
import pdb

class Test(object):
    def __init__(self,path,extension):
            """
            initializes a data object
            """
            self.basedir = path
            self.data_type = extension
            self.list_of_fastq_filepaths = self.get_data_files()
    
    def get_data_files(self):
        """
        returns all files
        """
        temp_list = []
        for path_name_tuple in os.walk(self.basedir):
            dir_name = path_name_tuple[0]
            for file_base_name in path_name_tuple[2]:
                if file_base_name.endswith(self.data_type):
                    temp_list.append(FilePath(os.path.join(dir_name,file_base_name)))
        return temp_list

#pdb.set_trace()
print Test('/Users/pczrr/Documents/Work/Project-Folders/Enzymatics/coding_tasks/sample_files/','.fastq').list_of_fastq_filepaths