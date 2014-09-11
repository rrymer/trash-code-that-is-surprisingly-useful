# -*- coding: utf-8 -*-
"""
Created on Sat Jun  7 08:53:38 2014

@author: pczrr

Program that answers this puzzler:

“Recently I had a visit with my mom and we realized that the two digits that 
make up my age when reversed resulted in her age. For example, if she’s 73, I’m 37. 
We wondered how often this has happened over the years but we got sidetracked 
with other topics and we never came up with an answer.

“When I got home I figured out that the digits of our ages have been reversible 
six times so far. I also figured out that if we’re lucky it would happen again 
in a few years, and if we’re really lucky it would happen one more time after 
that. In other words, it would have happened 8 times over all. So the question 
is, how old am I now?”


"""
##mods
import multiprocessing as mp
import time

##fxns
#def search(dif):
#    ##initialize counter
#    i=0
#    ##loop over second data set, and perform comparison
#    for x in xrange(0,1000,1):
#        x_old = x + dif
#        if str(x_old)[::-1] == str(x):
#            i=i+1
#        else:
#            continue
#    if i:
#        q.put((dif,i))

def rsearch(dif,age,i):    
    try: 
        assert age < 100 
    except AssertionError: 
        if i: 
            print dif, age, i
            return i
        else: 
            return 'None'
    a_old = age + dif
    if str(a_old)[::-1] == str(age):
        if not i: i += 1
        return rsearch(dif,age+1,i+1)
    else:
        return rsearch(dif,age+1,i)

def return_i(i):
#    print type(i)
    return i

##params/defs

#cands=[]
if __name__=='__main__':
    num_d={}
    i=0
    ##initialize queue:
#    q=mp.Queue(maxsize=100)
#    ##initialize Pool
#    p=mp.Pool(25)
#    ##jobs list for iterating throuh queue
#    jobs=[]
#    ##loop through something, multiprocessed    
#    for x in xrange(0,1000,1):
#        p.apply_async(search, args=(x,))
#        jobs.append(x)
#    p.close()
#    p.join()
#    ##use jobs list to iterate over queue
#    for j in jobs:
#        if q.empty():
#            continue
#        else:
#            cand=q.get()
#            num_d[cand[0]]=cand[1]
##    for dif in xrange(0,50,1):
##        search(dif)
##print cands
#    print 'done'
#    ##sort results dictionary    
#    l=[]
#    for k,v in num_d.iteritems():
#        l.append((k,v))
#    print sorted(l)
    for x in xrange(1,100,1):
        i=rsearch(x,0,0)
        if i:
            print 'i=' + str(i)
            num_d[x]=i
    print num_d
#        for h in hits:
#            num_d.append((x, h))