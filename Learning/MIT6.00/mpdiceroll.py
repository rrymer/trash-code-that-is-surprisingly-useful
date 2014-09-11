# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 19:39:29 2014

@author: pczrr
"""

#i=0
#l = []
#while i < 10:
#    print i 
#    l.append(i)
#    i += 1
#
#print len(l)

import random
import pylab
import multiprocessing as mp

def role_dice(numTrials):
    yes = 0.0
    for i in range(numTrials):
        for j in range(24):
            die1 = random.randrange(1,7)
            die2 = random.randrange(1,7)
#                fout.write(str(die1) + '\t' + str(die2) + '\n')
            if die1 == die2 == 6:
                yes += 1
                break
    results = (numTrials,yes/numTrials)
    q.put(results)

def showPlot1(data):
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    data should be a list of lists of tuples
    """ 
    for d in data:
        pylab.plot(d[0],d[1])
    pylab.title('trials vs ratio')
    pylab.xlabel('number of trials')
    pylab.ylabel('ratio')
    pylab.show()

p = mp.Pool(8)
q = mp.Queue(100)

data_x = []
data_y = []
jobs = []
for i in range(1,100000,10000):
    p.apply_async(role_dice, args=(i,))
    jobs.append(i)
p.close()
p.join()
print q.empty()
for j in jobs:
    print 'getting data for', j
    result = q.get(block=False)
    print result
    print 'got result'
    data_x.append(result[0])
    data_y.append(result[1])

showPlot1([(data_x,data_y)])

