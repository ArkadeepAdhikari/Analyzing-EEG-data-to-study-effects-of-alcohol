import os  #importing neccesary modules
import pandas as pd
import numpy as np

os.chdir(r"F:\eeg\subject1")  #setting path to subject folder
data1=pd.read_csv("co2a0000364.csv")#extacting subject data
data1=data1[(data1.stimulus=="S1obj")]  # filter data by stimulus

f = lambda x: str(x) if (len(str(x))==2)  else ("0"+str(x))
l=[f(x) for x in range(64)]
#restructuring column names to retain order in pivot
data1=data1.rename(columns=lambda x:("0"+str(x)) if (len(str(x))==1)  else x )
#pivot table for taking mean data across subjects over time
t=pd.pivot_table(data1,index=["timestamp"],values=l,aggfunc=[np.mean])

# some structural modifications
t = pd.DataFrame(t.to_records())
t.columns = [hdr.replace("('mean', ", "").replace(")", "") \
                     for hdr in t.columns]
t.to_csv("t.csv")#storing result as csv files


#repeating the same process for a control subject

path2=r"F:\eeg\subject2"+"\\"#setting path to subject folder
data2=pd.read_csv(path2+"co2c0000337.csv")#extacting subject data
data2=data2[(data2.stimulus=="S1obj")]  # filter data by stimulus

f = lambda x: str(x) if (len(str(x))==2)  else ("0"+str(x))
l=[f(x) for x in range(64)]
#restructuring column names to retain order in pivot
data2=data2.rename(columns=lambda x:("0"+str(x)) if (len(str(x))==1)  else x )
#pivot table for taking mean data across subjects over time
t2=pd.pivot_table(data2,index=["timestamp"],values=l,aggfunc=[np.mean])

# some structural modifications
t2 = pd.DataFrame(t2.to_records())
t2.columns = [hdr.replace("('mean', ", "").replace(")", "") \
                     for hdr in t2.columns]
t.to_csv("t.csv")#storing result as csv files
