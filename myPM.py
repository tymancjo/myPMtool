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

def fnt(size):
    matplotlib.rcParams.update({'font.size': size})
    

def tt(isPrint=False):
    fig = plt.figure('Team tasks')
    
    if isPrint:
        fig.set_size_inches(16.53, 11.69)
    
    fig.clear()

    a0 = plt.subplot(511)
    
    a1 = plt.subplot(523)

    a2 = plt.subplot(524)

    a3 = plt.subplot(525)

    a4 = plt.subplot(526)
    
    a5 = plt.subplot(527)

    a6 = plt.subplot(528)
    
    a7 = plt.subplot(515)
           
    P.gt(P.milestones, y_scale=[1,2,3,1,2,3,4,5,6,7,8,9], x_scale='w', ax=a0,
         clrs=['steelblue','purple','silver','steelblue',
               'green','silver','deepskyblue'])
    a0.set_title('Milestones')

    P.gt(P.m(1).tasks, x_scale='w', ax=a1)
    a1.set_title(P.m(1).nick)

    P.gt(P.m(2).tasks, x_scale='w', ax=a2)
    a2.set_title(P.m(2).nick)

    P.gt(P.m(3).tasks, x_scale='w', ax=a3)
    a3.set_title(P.m(3).nick)

    P.gt(P.m(4).tasks, x_scale='w', ax=a4)
    a4.set_title(P.m(4).nick)
    
    P.gt(P.m(5).tasks, x_scale='w', ax=a5)
    a5.set_title(P.m(5).nick)

    P.gt(P.m(6).tasks, x_scale='w', ax=a6)
    a6.set_title(P.m(6).nick)
       
   
    P.gt([t for t in P.infoHTML()[::-1] if t in P.listNoOwner()],
          x_scale='w', ax=a7, clrs=['silver']*len(P.listNoOwner()))
    a7.set_title('Without Owner')
    
    
    plt.tight_layout()
