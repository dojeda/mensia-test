#!/usr/bin/env python3

import numpy as np
import scipy.interpolate as spi
import matplotlib.pyplot as plt
from matplotlib import cm
from coordinates1020 import get_1020coords

def myplot(values, electrodes, axis, head=True):
    values = np.asarray(values)
    electrodes = np.asarray(electrodes)
    assert(values.size == electrodes.size)

    all_coords = get_1020coords()
    Xe = []
    Ye = []
    Ze = []

    for ei in electrodes:
        x,y,z = all_coords[ei]
        Xe.append(x)
        Ye.append(y)
        Ze.append(z)

    Xe = np.asarray(Xe)
    Ye = np.asarray(Ye)
    Ze = np.asarray(Ze)

    gridpoints = np.linspace(-1,1,250)
    Xi,Yi = np.meshgrid(gridpoints, gridpoints)

    rbf = spi.Rbf(Xe,Ye,values,epsilon=1) # RBF ignoring Z coordinates
    Vi = np.ma.masked_array(rbf(Xi,Yi))

    # Mask out of head values
    Vi[Xi**2 + Yi**2 > 1] = np.ma.masked

    cmap = cm.jet
    axis.pcolor(Xi,Yi,Vi,cmap=cmap,vmin=0,vmax=1)

    if head:
        # plot fake head
        circle = np.linspace(0,2*np.pi,1e3)
        xhead = np.sin(circle)
        yhead = np.cos(circle)
        axis.plot(xhead,yhead,color='k',linewidth=3)

    # plot projection of electrodes on Z=0
    axis.plot(Ye,Xe,'bo')
    axis.set_xlim((-1.1,1.1))
    axis.set_ylim((-1.1,1.1))


def main():
    import matplotlib.pyplot as plt

    electrodes = 'O1 O2 Oz Cz C3 C4 Fz F8 F7 Fpz'.split()
    values = np.random.random(size=len(electrodes))
    fig,ax = plt.subplots(1,1)

    myplot(values,electrodes,ax,head=True)

    plt.show()

if __name__ == '__main__':
    main()
