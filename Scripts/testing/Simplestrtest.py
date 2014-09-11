# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 17:00:10 2013

@author: rrymer
"""

color = 'more than one letter to look for'
if ('f' or 'l' or 'm' or 'o') in color.lower():
    print "Works here"
else: print "WTF?!"