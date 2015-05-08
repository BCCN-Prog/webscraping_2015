
import numpy as np
import pickle
import os
import sys
#import bad
#print(__file__)
mydir = os.path.abspath(os.path.dirname(__file__))

print(mydir)

lookupmatrix = pickle.load(open( \
                               mydir +'/accuweather_location_codes.dump','rb'))

lookuplist = lookupmatrix.tolist()

