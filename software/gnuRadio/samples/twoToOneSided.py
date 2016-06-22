# Take an array of powers calculated by the welch method.
# Return the one-sided view.
# Warning:  this is the correct thing to do ONLY when the input voltages
# are all real numbers.
import numpy as np

def twoToOneSided(vector, debug=False):
    if debug: print "vector=",vector
    length = len(vector)
    left = vector[:length/2]
    left_reversed = np.fliplr([left])[0]
    if debug: print "left_reversed=",left_reversed
    right = vector[length/2:]
    if debug: print "right=",right
    sum = left_reversed+right
    return sum

ps = np.arange(10, dtype=np.complex64)
answer = twoToOneSided(ps, debug=True)
print "answer=",answer
