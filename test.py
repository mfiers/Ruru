#!/usr/bin/env python

import random

import numpy as np
import pandas as pd

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

import leip

from ruru.feature import *
from ruru.view import *

flist = []

for x in range(8):
    start = random.randint(0, 500)
    length = random.randint(20, min(120, 600-start))
    stop = start + length
    flist.append(Feature('x', start, stop, score = random.randint(0,10)))

score_array = pd.Series(np.random.randn(100))

flist.append(ScoreFeature('test_1', 100, 450, 1, score=score_array))

flist.append(Feature('test_2', 430, 500, -1))
flist.append(Feature('test_2', 380, 420, 1))
flist.append(FeatureGene('gene1', 200, 500, 1,
                          children=[FeatureExon('', 220, 250),
                                    FeatureExon('', 280, 300),
                                    FeatureExon('', 400, 480),
                                    ]))


plt.figure(figsize=(12,3))
ax = plt.subplot(111)
plt.tight_layout()
view = View(ax, -10, 610, score_max=10)
view.draw(flist)
plt.savefig('test.png', dpi=200)

