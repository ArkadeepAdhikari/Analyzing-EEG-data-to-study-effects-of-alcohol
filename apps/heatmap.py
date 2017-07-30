
import os #importing required modules
import pandas as pd
import numpy as np
import seaborn as sns

os.chdir(r"F:\eeg\subject1\groups")#setting path to mean data
data1=pd.read_csv("cons2nomatch.csv")#selecting the files of required group and stimulus
del data1["timestamp"]# deleting unneccesary columns
data1=data1.T    #transposing the dataframe
data1=data1.iloc[::-1] # this is used to reverse the dataframe indexes to customise our plot

# plotting the heatmap
a= sns.heatmap(data1,cmap="YlGnBu",xticklabels=25, yticklabels=5)