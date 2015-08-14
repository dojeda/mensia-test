#!/usr/bin/env python3

import pandas as pd
import numpy as np
import scipy.stats as sps
import rpy2.robjects as robj
import rpy2.robjects.pandas2ri
from rpy2.robjects.packages import importr
import matplotlib.pyplot as plt

from ptest import permutation_test

datafile = 'data/full_data.csv'

data = pd.read_csv(datafile)

features = data.feature.unique()
groups   = data.group.unique()
electrodes = 'O1 O2 Oz Cz C3 C4 Fz F8 F7 Fpz'.split()

# # Let's make a chart of available data
# robj.pandas2ri.activate()
# R_chart_code = robj.r('''
# function(df) {

# require(ggplot2)
# require(GGally)

# gp = ggpairs(df[,c('group','subject','time')])

# png('dataset-pairs.png',pointsize=24)
# print(gp)
# dev.off()

# }
# ''')
# data_r = robj.conversion.py2ri(data)
# R_chart_code(data_r)

# plt.imshow(plt.imread('dataset-pairs.png'))
# plt.show()
print(data.groupby(['group','time','subject']).count())
