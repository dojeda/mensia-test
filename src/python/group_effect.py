#!/usr/bin/env python3

import pandas as pd
import numpy as np
import scipy.stats as sps
from ptest import permutation_test

datafile = 'data/full_data.csv'

data = pd.read_csv(datafile)

features = data.feature.unique()
groups   = data.group.unique()
electrodes = 'O1 O2 Oz Cz C3 C4 Fz F8 F7 Fpz'.split()

## Question: is there an effect of time on the mean value of all electrodes?
print('Q: time vs mean value of features')
for feat_i in features:
    fi_t1 = data.ix[np.all((data.time=='T1',data.feature==feat_i),axis=0),
                    electrodes].mean(axis=1)
    fi_t2 = data.ix[np.all((data.time=='T2',data.feature==feat_i),axis=0),
                    electrodes].mean(axis=1)
    tstat,pvalue = sps.ttest_rel(np.asarray(fi_t1),
                                 np.asarray(fi_t2))
    print('Feature {}: p-value={:1.3f} {}'.format(feat_i,pvalue,'*' if pvalue < 0.01 else ''))

## Question: is there an effect of time and group on the mean value of all electrodes?
print('Q: (time and group) vs mean value of features')
print('             {}'.format('  '.join(groups)))
for feat_i in features:
    print('Feature',feat_i,end='   ')
    for gi in groups:
        fi_t1 = data.ix[np.all((data.time=='T1',data.feature==feat_i,data.group==gi),axis=0),
                    electrodes].mean(axis=1)
        fi_t2 = data.ix[np.all((data.time=='T2',data.feature==feat_i,data.group==gi),axis=0),
                    electrodes].mean(axis=1)
        tstat,pvalue = sps.ttest_ind(np.asarray(fi_t1),
                                     np.asarray(fi_t2))
        print('{:1.3f}{}'.format(pvalue,'[*]' if pvalue < 0.01 else '   '),end=' ')
    print()

## Question: is there a difference between the two groups when considering the mean value of all electrodes?
print('Q: group vs mean value of features')
for feat_i in features:
    fi_g1 = data.ix[np.all((data.group=='group-1',data.time=='T1',data.feature==feat_i),axis=0),
                    electrodes].mean(axis=1)
    fi_g2 = data.ix[np.all((data.group=='group-2',data.time=='T1',data.feature==feat_i),axis=0),
                    electrodes].mean(axis=1)
    tstat,pvalue = sps.ttest_ind(np.asarray(fi_g1),
                                 np.asarray(fi_g2))
    print('Feature {}: p-value={:1.3f} {}'.format(feat_i,pvalue,'*' if pvalue < 0.01 else ''))

## Question: is there a difference between the two groups when considering each electrode
print('Q: features per electrode, is there a difference by group?')
print('               {}'.format('       '.join(electrodes)))
for feat_i in features:
    print('Feature',feat_i,end='   ')
    for elec_i in electrodes:
        fi_g1 = data.ix[np.all((data.group=='group-1',data.time=='T1',data.feature==feat_i),axis=0),
                        elec_i]
        fi_g2 = data.ix[np.all((data.group=='group-2',data.time=='T1',data.feature==feat_i),axis=0),
                        elec_i]
        # tstat,pvalue = sps.ttest_ind(np.asarray(fi_g1),
        #                              np.asarray(fi_g2))
        pvalue = permutation_test(np.asarray(fi_g1),
                                  np.asarray(fi_g2))
        print('{:1.3f}{}'.format(pvalue,'[*]' if pvalue < 0.01 else '   '),end=' ')
    print()

## Question: is there a difference between time when considering each electrode
print('Q: features per electrode, is there a difference by time? (group 1)')
print('               {}'.format('       '.join(electrodes)))
for feat_i in features:
    print('Feature',feat_i,end='   ')
    for elec_i in electrodes:
        fi_g1 = data.ix[np.all((data.group=='group-1',data.time=='T1',data.feature==feat_i),axis=0),
                        elec_i]
        fi_g2 = data.ix[np.all((data.group=='group-1',data.time=='T2',data.feature==feat_i),axis=0),
                        elec_i]
        # tstat,pvalue = sps.ttest_ind(np.asarray(fi_g1),
        #                              np.asarray(fi_g2))
        pvalue = permutation_test(np.asarray(fi_g1),
                                  np.asarray(fi_g2))
        print('{:1.3f}{}'.format(pvalue,'[*]' if pvalue < 0.01 else '   '),end=' ')
    print()

## Question: is there a difference between time when considering each electrode
print('Q: features per electrode, is there a difference by time? (group 2)')
print('               {}'.format('       '.join(electrodes)))
for feat_i in features:
    print('Feature',feat_i,end='   ')
    for elec_i in electrodes:
        fi_g1 = data.ix[np.all((data.group=='group-2',data.time=='T1',data.feature==feat_i),axis=0),
                        elec_i]
        fi_g2 = data.ix[np.all((data.group=='group-2',data.time=='T2',data.feature==feat_i),axis=0),
                        elec_i]
        # tstat,pvalue = sps.ttest_ind(np.asarray(fi_g1),
        #                              np.asarray(fi_g2))
        pvalue = permutation_test(np.asarray(fi_g1),
                                  np.asarray(fi_g2))
        print('{:1.3f}{}'.format(pvalue,'[*]' if pvalue < 0.01 else '   '),end=' ')
    print()
