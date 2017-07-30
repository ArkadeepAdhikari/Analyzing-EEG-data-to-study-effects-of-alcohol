import os # importing neccessary modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns

os.chdir(r"F:\eeg\subject1")
path1=r"F:\eeg\subjectwisedata"+"\\" # setting the path to input data
fl=os.listdir(path1)# this path contains all the data for alcoholic and control subjects
fl=np.sort(fl)
f1=np.append(fl[0:65],fl[109:121])# selecting alcoholic data
f2=np.append(fl[65:109],fl[121:122])# selecting control data

data1=pd.DataFrame()
data2=pd.DataFrame()

for df1 in f1:
    print(df1)# to see the stage of progress of the code
    data1=data1.append(pd.read_csv(path1+df1))

data1=data1[(data1.stimulus=="S2nomatch")]  # filter data by stimulus

#restructuring column names to retain order in pivot
f = lambda x: str(x) if (len(str(x))==2)  else ('0'+str(x))
l=[f(x) for x in range(64)]
data1=data1.rename(columns=lambda x:('0'+str(x)) if (len(str(x))==1)  else x )
#pivot table for taking mean data across subjects over time
t=pd.pivot_table(data1,index=["timestamp"],values=l,aggfunc=[np.mean])


t = pd.DataFrame(t.to_records()) # some structural modifications
t.columns = [hdr.replace("('mean', ", "").replace(")", "") \
                     for hdr in t.columns]
t1=t


#repeating the same process for a control subject

for df2 in f2:
    print(df2)# to see the stage of progress of the code
    data2=data2.append(pd.read_csv(path1+df2))


data2=data2[(data2.stimulus=="S2nomatch")]  # filter data by stimulus

#restructuring column names to retain order in pivot
f = lambda x: str(x) if (len(str(x))==2)  else ('0'+str(x))
l=[f(x) for x in range(64)]
data2=data2.rename(columns=lambda x:('0'+str(x)) if (len(str(x))==1)  else x )
#pivot table for taking mean data across subjects over time
t2=pd.pivot_table(data2,index=["timestamp"],values=l,aggfunc=[np.mean])


t2 = pd.DataFrame(t2.to_records())# some structural modifications
t2.columns = [hdr.replace("('mean', ", "").replace(")", "") \
                     for hdr in t2.columns]

#performing significance testing 

import scipy.stats as stats # importing module for significance testing

data3=pd.DataFrame()
cols=t1.columns.values.tolist()
cols=cols[1:65]

for c in cols:
    print(c)# to see the stage of progress of the code
    t,p=stats.ttest_ind(t1[str(c)],t2[str(c)], equal_var=False)
    data4=pd.DataFrame([t],[p])
    data4 = data4.reset_index()
    data4.columns=["p","t"]# naming columns for p-values and t-values
    data4["channel"]=c
    data3=data3.append(data4)
data3.to_csv("significance.csv")# storing significance results to csvs