#!/usr/bin/env python3

import numpy as np
import scipy.interpolate as spi
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import cm
from coordinates1020 import get_1020coords

# I did not write this utility function, this was taken from stack overflow at
# http://stackoverflow.com/a/16836182/227103
def make_colormap(seq):
    '''Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    '''
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)

def plot1020(values, electrodes, axis, head=True):
    ''' Interpolate and plot a color array of the scalp
    values: values to plot, excepts values between 0 and 1 (e.g. p values)
    electrodes: same size as values, the observed scalp electrodes
    axis: axis where the plot will be done
    head: plot the head reference
    returns a plot object that may be used for plt.colorbar
    the colormap used is a diverging map that changes around 0.1 in order to
    mark statistical significance
    '''
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

    #cmap = cm.bwr
    c = mcolors.ColorConverter().to_rgb
    cmap = make_colormap([c('red'), c('white'), 0.1, c('white'), c('blue')])
    cres = axis.pcolor(Xi,Yi,Vi,cmap=cmap,vmin=0,vmax=1)

    if head:
        # plot fake head
        circle = np.linspace(0,2*np.pi,1e3)
        xhead = np.sin(circle)
        yhead = np.cos(circle)
        axis.plot(xhead,yhead,color='k',linewidth=3)

    # plot projection of electrodes on Z=0
    axis.plot(Ye,Xe,'go')
    axis.set_xlim((-1.1,1.1))
    axis.set_ylim((-1.1,1.1))

    return cres


def main():
    import matplotlib.pyplot as plt

    electrodes = 'O1 O2 Oz Cz C3 C4 Fz F8 F7 Fpz'.split()
    values = np.random.random(size=len(electrodes))
    #values = np.linspace(0,1,10)
    fig,ax = plt.subplots(1,1)

    cres = plot1020(values,electrodes,ax,head=True)

    cbar = fig.colorbar(cres)
    cbar.set_label('p value')
    plt.show()

if __name__ == '__main__':
    main()
