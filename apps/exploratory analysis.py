
import os # imports neccessary modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.chdir(r"F:\eeg\subject1")#setting the path to subject folder
data1=pd.read_csv("co2a0000364.csv")# pulling data for a subject
#data1.head()
data1=data1[data1.trial_num==7]  # fixes the trial number 
data1.plot(x='timestamp', y=['0']) # fixes the channel and plots the timeseries

#studying differences of the 3 stimuli on a subject: mean of 3 selected trials

os.chdir(r"F:\eeg\subject1")
data1=pd.read_csv("co2a0000364.csv")# extracting subect data
#filtering the trials needed
data1=data1[(data1.trial_num==7)|(data1.trial_num==2)|(data1.trial_num==17)]
t=pd.pivot_table(data1,index=["timestamp"],values=["0"],\
               columns=["stimulus"],aggfunc=[np.mean])#creating pivot table by mean values

t = t.rename_axis(None)
#list(t)  # helps to see the column header of dataframe t
t = pd.DataFrame(t.to_records())
t.columns=["timestamp","S1obj","S2match","S2nomatch"]# setting the column names
#list(t)  # helps to see the column header of dataframe t

t.plot(x='timestamp', y=['S1obj',"S2match","S2nomatch"])#plotting the data by stimulus

