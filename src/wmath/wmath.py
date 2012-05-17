
__all__=['weighted_choice','render_points','argpick','argmin','argmax','binary_search', 'spline_lp_norms', 'spline_lp_distances']

from random import uniform

import collections
from Queue import Queue
from math import sqrt,sin,cos,tan,pi

import Lp_spline3
import numpy
import pylab

'''
Like python's builtin random.choice, but with weights.
The function randomly chooses an integer i, 0 <= i < len(weights). Choosing the integer i has a probability equal to weights[i] / sum(weigths).

If choiceSet is None, returns the chosen integer i.
If choiceSet is not None, returns choiceSet[i], with i as above.

'''
def weighted_choice(weights, choiceSet=None):
    r = uniform(0, sum(weights))

    #TODO FORLOOPS NO!!!!!
    for i, weight in enumerate(weights):
        r -= weight
        if(r < 0):
            if choiceSet is None:
                return i
            else:
                return choiceSet[i]

    assert False, "This should not happen."

def render_points(fx,fy,dfx,dfy,dl,l_tot,t=0):
    """
    @param fx,fy the parametric function
    @param dfx,dfy the derivative of the parametric function
    @param Dl the wanted steplength
    @param wanted totallength

    Returns approriate points from t=0:t_length of the parametricfunction
    """
    l=0
    yield (fx(t),fy(t),l)
    while(l<l_tot):
        df=lambda t:sqrt(dfx(t)**2+dfy(t)**2)
        dt=dl/max(df(t),0.000000001) #to avoid divide by zero (mostly att start)
        t+=dt
        l+=dl
        yield (fx(t),fy(t),l)

"""
points = list(render_points(
        lambda t:2*cos(t)+cos(8*t),
        lambda t:2*sin(t)+sin(8*t),
        lambda t:-2*sin(t)-8*sin(8*t),
        lambda t:2*cos(t)+8*cos(8*t),
        0.05,
        50))
"""
"""
points = list(render_points(
        lambda t:cos(t),
        lambda t:sin(t),
        lambda t:sin(t),
        lambda t:-cos(t),
        0.1,
        2*pi,
        ))
"""
#pylab.plot(map(lambda point:point[0],points),map(lambda point:point[1],points),'+')
#pylab.show()

class function:
    """
    Usally very computional heavy function as example featureresponses or such that one wants to save for later use

    Using numpy.savez (and some surrounding structure)

    All the variables are vectors and the response is the value of the function for a product (as in algebra) of all the variables
    """
    def __init__(self,variables,f):
        """

        """
        assert isinstance(variables,dict)
        assert isinstance(f,collections.Callable)
        self.variables=variables

    def calculate(self):
        pass

    def load(self,filename):
        """
        Load from filename
        """
        pass

    def save(self):

        pass

    def plot(self):
        """
        Plot with approriate labels on the variables and such
        """
        pass

def argpick(picker,f,seq):
    return min(map(lambda s:(f(s),s),seq))[1]
def argmin(f,seq):
    return argpick(min,f,seq)
def argmax(f,seq):
    return argpick(max,f,seq)

class spec_range():
    """
    NOTE only used to compare int and list like 'all in range bigger/smaller than int'>/< or 'range has int inside' =
    """
    def __init__(self,a,b):
        self.a=a
        self.b=b

    def __assert_compare_value(self,value):
        assert(isinstance(value,(int,long,float)))
        
    def __eq__(self,other):
        self.__assert_compare_value(other)
        return self.a<other and other<self.b

    def __lt__(self,other):
        self.__assert_compare_value(other)
        return other<self.a

    def __gt__(self,other):
        self.__assert_compare_value(other)
        return self.b<other 

def binary_search(get_value,goal,seq):
    """
        To evalute as few seq_elements as possible and find 
        
        @param seq sorted according to get_value
        @param get_value : seq_elem->value
        @param goal int or spec_range or something that compares (<,=,>) with value
        
        returns the first element satisfying goal(get_value(seq_elem))
    """
    assert(len(seq)!=0)

    if(len(seq)==1): #basecase,check if the last man standing is right
        if(goal(get_value(seq[0]))):
            return seq[0]
        else:
            return None
    else: #recursion
        mid_index=int(len(seq)/2) #keep 'int' for compability with python3
        mid_elem=seq[mid_index]
        mid_value=get_value(mid_elem)
        if(goal>mid_value):
            return binary_search(get_value,goal,seq[(mid_index+1):])
        elif(goal<mid_value):
            return binary_search(get_value,goal,seq[:mid_index])
        else: #found a value
            return mid_elem #basecase

def l2_distances_inverse(polynomials1, polynomials2, l):
    d = l2_distances_between_third_degree_polynomials_with_no_constant_terms(polynomials1, polynomials2, 1)
    d[numpy.where(d == 0)] = abs(d[numpy.where(d != 0)]).min()*1E-6 # HACK: Preventdivision by zero
    return 1.0/d

def l2_distances_between_third_degree_polynomials_with_no_constant_terms(polynomials1, polynomials2, l):
    l3 = l**3
    l4 = l**4
    l5 = l**5
    l6 = l**6
    l7 = l**7

    diff = polynomials1 - polynomials2

    return (diff[:,2]**2/3*l3 + diff[:,1]*diff[:,2]/2*l4 + (diff[:,1]**2 + 2*diff[:,0]*diff[:,2])/5*l5 + diff[:,0]*diff[:,1]/3*l6 + diff[:,0]**2/7*l7)**0.5

Lp_norm_functions = [
    Lp_spline3.L0_spline3,
    Lp_spline3.L1_spline3,
    Lp_spline3.L2_spline3,
    Lp_spline3.L3_spline3,
    Lp_spline3.L4_spline3,
    Lp_spline3.L5_spline3,
    Lp_spline3.L6_spline3,
    Lp_spline3.L7_spline3,
    Lp_spline3.L8_spline3
]


def spline_lp_norms(polynomials, l, p):
    if len(polynomials.shape) == 1:
        polynomials.resize(1, polynomials.size)
    a = polynomials[:,0]
    b = polynomials[:,1]
    c = polynomials[:,2]
    return (Lp_norm_functions[p](a, b, c, l))**(1.0/p)

def spline_lp_distances(pols1, pols2, l, p):
    return spline_lp_norms(pols1-pols2, l, p)
