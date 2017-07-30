
import os #importing required modules
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

os.chdir(r"F:\eeg\subject1")# giving path to data folder
data1=pd.read_csv("co2a0000364.csv")#extracting required files
data1.head()#to see the structure of the data uploaded
data1=data1[data1.trial_num==2]# fixing a trial number
del data1["subject_id"]
del data1["alcoholic"]
del data1["stimulus"]
del data1["timestamp"]#deleting unneccesary columns
Z=data1.corr()
Z = Z.as_matrix()#converting data frame to matrix

# printing correlation network

import networkx as nx  # to build the graph network
G=nx.from_numpy_matrix(np.array(Z))
nx.draw(G, with_labels=True)#plotting the graph


## printing covariance triangle
#we use seaborn for this plot

sns.set(style="white")
corr = Z

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3,
            square=True, xticklabels=5, yticklabels=5,
            linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)


