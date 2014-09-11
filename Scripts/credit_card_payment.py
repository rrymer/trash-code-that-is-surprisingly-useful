# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 20:44:22 2014

@author: pczrr

min payment = minpayment rate * balance
interest paid = APR/12 * Balance
Principal paid = minpayment - interest paid
remaining balance = balance - principal paid


    

"""

def payoff(payment,bal):
    tot_paid=0
    months = 0
    while months < 12:
        months += 1
        int_paid = APR/12 * bal
        pri_paid = payment  - int_paid
        if bal - pri_paid >= bal:
            return months,bal
        else:
            bal = bal - pri_paid
        tot_paid += pri_paid + int_paid
#        print 'month', month + 1, round(bal,2), round(pri_paid,2)
#    print 'year end:', round(tot_paid,2), round(bal,2)
    return bal
    
init_bal = 32000
APR = 0.2
term = [x for x in range(12)]
i=1
while x <= init_bal:
    bal = init_bal
    bal = payoff(x,bal)
    if bal <= 0:
        print i, 'monthly payment should be:$', x, 'months needed:12', 'with a final balance of $', round(bal,2)
        break
    x += 0.01
    i += 1


lb_p = init_bal/12
ub_p = (init_bal*(1+(APR/12))**12)/12
payment = (ub_p + lb_p)/2
i=1
bal= init_bal
months = None
#print bal
while abs(bal) >= 0.01:
    bal = init_bal
    bal = payoff(payment,bal)
    if bal > 0:
        print 'payment too low'
        lb_p = payment
    elif bal < 0:
        print 'payment too high'
        ub_p = payment
    payment = (ub_p + lb_p)/2
    i += 1

print i, round(payment,2), round(bal,2)