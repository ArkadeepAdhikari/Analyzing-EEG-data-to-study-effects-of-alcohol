
import os  #importing neccesary modules
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

os.chdir(r"F:\eeg\subject1\groups")#setting path to mean data
data1=pd.read_csv("cons2nomatch.csv")#selecting the files of required group and stimulus
del data1["timestamp"]# deleting unneccesary columns

#performing some structural changes
x=np.arange(len(data1.columns))
y=data1.index
X,Y=np.meshgrid(x,y)#creating a numpy coordinate matrix
Z=data1
#plotting the surface plot
fig=plt.figure()
ax=fig.add_subplot(111,projection="3d")
ax.plot_surface(X,Y,Z)

