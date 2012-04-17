
__all__=['weighted_choice','argpick','argmin','argmax','binary_search']

from random import uniform

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

