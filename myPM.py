# Import statements
# PM toolset library
from myPMlib.myPMlib import *
import matplotlib

if __name__ == '__main__':
    # Some hard coded definition for developemnt only
    pf = 'projekt.save'
    P = loadObj(pf)
    matplotlib.rcParams.update({'font.size': 6})