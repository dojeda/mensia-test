#!/usr/bin/env python3

import numpy as np

def permutation_test(X1, X2, nperm=1000):
    values = np.concatenate((np.asarray(X1),
                             np.asarray(X2)))
    differences = np.zeros(nperm)
    nX1 = X1.size
    nX2 = X2.size
    indices = np.arange(nX1 + nX2)
    for i in range(nperm):
        np.random.shuffle(indices)
        differences[i] = values[indices[:nX1]].mean() - values[indices[nX1:]].mean()

    original_diff = np.abs(X1.mean() - X2.mean())
    p = np.sum(np.abs(differences) >= original_diff) / nperm

    return p, original_diff, differences

def plot_permutation_test(p, original_diff, differences, axis):

    _,bins,patches = axis.hist(differences,bins=100,color='b',edgecolor='none')
    axis.axvline(x=original_diff,color='m',linewidth=2)

    # set color of tail
    for pi in np.where(np.abs(bins) >= original_diff)[0]:
        patches[pi-1].set_color('r')

    axis.set_title('Permutation test p-value={:.3f}'.format(p))


def interaction_plot(data, feature, electrode, factor1, factor2, axis):
    grouped_data = data[data['feature']==feature].groupby([factor1,factor2])
    mean_electrode = grouped_data[electrode].mean()
    std_electrode  = grouped_data[electrode].std()

    f1values = data[factor1].unique()
    f2values = data[factor2].unique()
    line_styles  = ['-', '--', '-.', ':']
    line_colors  = list('brgcmyk')
    line_markers = list('os^vx+')

    for i,fi in enumerate(f1values):
        ls = line_styles[i % len(line_styles)]
        lc = line_colors[i % len(line_colors)]
        lm = line_markers[i% len(line_markers)]
        axis.plot(mean_electrode[fi],color=lc,linestyle=ls,marker=lm,label=fi)
        # axis.errorbar(x=np.arange(f2values.size),
        #               y=mean_electrode[fi],
        #               yerr=std_electrode[fi],
        #               color=lc,linestyle=ls,marker=lm)

    axis.legend(title=factor1)
    axis.set_xticks(np.arange(0,f2values.size))
    axis.set_xlim((-0.1,f2values.size - .9))
    axis.set_xticklabels(f2values)
    axis.set_ylabel('Mean of {}'.format(electrode))
    axis.set_xlabel(factor2)
    axis.set_title('{} interactions for {}'.format(feature,electrode))


def main():
    import matplotlib.pyplot as plt
    np.random.seed(0)
    fig,ax = plt.subplots(2,1)

    X1 = np.random.normal(loc=1.1 , scale=0.1, size=100)
    X2 = np.random.normal(loc=1.15, scale=0.1, size=150)

    p, odiff, diffs = permutation_test(X1,X2,10000)
    plot_permutation_test(p,odiff,diffs,ax[0])

    p, odiff, diffs = permutation_test(X1,X2-0.025,10000)
    plot_permutation_test(p,odiff,diffs,ax[1])

    plt.show()

if __name__ == '__main__':
    main()
