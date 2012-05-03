
__all__=['weighted_choice','argpick','argmin','argmax','binary_search']

from random import uniform

import collections
from Queue import Queue


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



def render_points(fx,fy,dfx,dfy,Dl,length,thickness=(lambda l:1)):
    """
    @param fx,fy the parametric function
    @param dfx,dfy the derivative of the parametric function
    @param Dl the wanted steplength
    @param wanted totallength

    Returns approriate points from t=0:t_length of the parametricfunction
    """
    l=0
    t=0
    df=lambda t:math.sqrt(dfx**2+dfy**2)
    while(l<length):
        print "bajs"

print render_points(lambda t:t,lambda t:t**2,lambda t:1,lambda t:2*t,0.1,5)





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

