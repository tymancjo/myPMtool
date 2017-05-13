# Import statements
# PM toolset library
from myPMlib.myPMlib import *
import matplotlib

if __name__ == '__main__':
    # Some hard coded definition for developemnt only
    pf = 'projekt.save'
    P = loadObj(pf)
    matplotlib.rcParams.update({'font.size': 6})

# just note
# P.gt(l[::-1], x_scale='w',text=[t.getOwnerName() for t in l[::-1]], y_labels=['{} [{}]'.format(x.name, P.getTaskBy_iD(x.iD)) for x in l[::-1]])