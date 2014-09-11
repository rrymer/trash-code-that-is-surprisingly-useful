# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 08:44:52 2014

@author: pczrr

Implement the evaluate_poly function. This function evaluates a polynomial function for the given x value. It takes in a tuple of numbers poly and a number x. By number, we mean
that x and each element of poly is a float. evaluate_poly takes the polynomial represented
by poly and computes its value at x. It returns this value as a float.

(ax^0,bx^1,...,yx^n)

"""

def evaluate_poly(poly,x):
    """
    Computes the polynomial function for a given value x. Returns that value. Example:
    >>> poly = (0.0, 0.0, 5.0, 9.3, 7.0) # f(x) = 7.0x4 + 9.3x3 + 5.0x2
    >>> x = -13
    >>> print evaluate_poly(poly, x) # f(-13) = 7.0(-13)4 + 9.3(-13)3 + 5.0(-13)2 180339.9
    poly: tuple of numbers, length > 0
    x: number
    returns: float
    """
    ##get polymnomial order
    order = len(poly)
    ##check that len and polynomial will work in function
    assert order > 0
    ##initialize accumulators
    value=poly[0]
    n=1
    ##calculate value loop
    while n <= order-1:
#        print 'n = {} coeff = {} term = {}'.format(n,poly[n],poly[n]*x**n)
        value += poly[n]*x**n
        n += 1
    return value

def compute_deriv(poly):
    """
    Computes and returns the derivative of a polynomial function. If the
    derivative is 0, returns (0.0,).
    Example:
    >>> poly = (-13.39, 0.0, 17.5, 3.0, 1.0)    # x4 + 3.0x3 + 17.5x2 - 13.39
    >>> print compute_deriv(poly)
    (0.0, 35.0, 9.0, 4.0)
    poly: tuple of numbers, length > 0
    returns: tuple of numbers
    """
    ##get polymnomial order
    order = len(poly)
    ##check that len and polynomial will work in function
    assert order > 0
    ##check to see if there is anything to calculate
    if order == 1:
        return 0
    ##initialize accumulators
    deriv=[]
    n=1
    while n <= order-1:
        print 'n = {} coeff = {}'.format(n,poly[n])
        deriv.append( n*poly[n] )
        print 'current deriv =',deriv
        n += 1
    return tuple(deriv)

def calculate_new_guess(x,poly,deriv):
    fofx=evaluate_poly(poly,x)
    fprimeofx=evaluate_poly(deriv,x)
    new_guess = x - (fofx/fprimeofx)
    return new_guess
    
def is_not_root(poly,x,precision):
    if abs(evaluate_poly(poly,x)) <= precision:
        return False
    else:
        return True

def compute_root(poly,guess,precision):
    """
    Uses Newton's method to find and return a root of a polynomial function.
    Returns a tuple containing the root and the number of iterations required to
    get to the root.
    Example:
    >>> poly = (-13.39, 0.0, 17.5, 3.0, 1.0)
    >>> x_0 = 0.1
    >>> epsilon = .0001
    >>> print compute_root(poly, x_0, epsilon)
    (0.80679075379635201, 8)
    poly: tuple of numbers, length > 1.
    Represents a polynomial function containing at least one real root.
    The derivative of this polynomial function at x_0 is not 0.
    x_0: float
    epsilon: float > 0
    returns: tuple (float, int)
    
    compute value at init_guess
    test value
    compute derivative
    compute value at derivative
    calculate new guess
    """
    ##copy guess just in case    
    x = guess
    ##get deriv ONCE, even if we don't need it
    deriv=compute_deriv(poly)
    ##initialize accumulator
    i=0
    ##run loop
    while is_not_root(poly,x,precision):
        print 'guessing again...'
        x=calculate_new_guess(x,poly,deriv)
        print 'new guess =',x
        i += 1
    return (x,i)
    
#    poly = (0.0, 0.0, 5.0, 9.3, 7.0)
#    x=-13
#    value=evaluate_poly(poly,x)
#    print 'value of polynomial at guess {} = {}'.format(i,value)
    
#    poly = (-13.39, 0.0, 17.5, 3.0, 1.0)
#    x=10
#    deriv=compute_deriv(poly)
#    print 'derivative of polynomial =', deriv
    
poly = (-13.39, 0.0, 17.5, 3.0, 1.0)
print compute_root(poly,0.1,0.0001)