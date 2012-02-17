from random import uniform

'''
Like python's builtin random.choice, but with weights.
The function randomly chooses an integer i, 0 <= i < len(weights). Choosing the integer i has a probability equal to weights[i] / sum(weigths).

If choiceSet is None, returns the chosen integer i.
If choiceSet is not None, returns choiceSet[i], with i as above.

'''
def weighted_choice(weights, choiceSet=None):
    r = uniform(0, sum(weights))

    for i, weight in enumerate(weights):
        r -= weight
        if(r < 0):
            if choiceSet is None:
                return i
            else:
                return choiceSet[i]

    assert False, "This should not happen."
