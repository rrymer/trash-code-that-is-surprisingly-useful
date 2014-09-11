# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 19:07:48 2014

@author: pczrr

bisection search
"""

def rsearch(x,g,h,l,cnt):
    if abs(g**2 - x) <= e:
        return (x,g,cnt)
    elif g**2 > x:
        cnt += 1
        h = g
        g = (h+l)/2
        return rsearch(x,g,h,l,cnt)
    elif g**2 < x:
        cnt += 1
        l = g
        g = (h+l)/2
        return rsearch(x,g,h,l,cnt)

results = {}
minp = 1
maxp = 0.000001
e = maxp
i = 1
while e <= minp:
    e
    for x in xrange(1,100,1):
        x = float(x)
        try:
            ans=rsearch(x,x/2,x,0,0)
            with open('/tmp/fun.txt','a') as fout:
                fout.write('{},{},{},{},{}'.format(e,ans[0],ans[1],ans[2],i) + '\n')
        except RuntimeError, e:
            print x
            print e
            continue
    i += 1
    e = maxp*2**i
#print rsearch(9.,4.5,9.,0,0)
        