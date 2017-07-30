import os  #importing neccesary modules
import pandas as pd
import numpy as np

os.chdir(r"F:\eeg\processed") #setting path containing data for all trials
to_dir=r"F:\eeg\subjectwisedata"+"\\" #setting path for storing resulting subject-wise data

p=os.listdir(".")#making a list of files of subjects present
for pi in p: #to enter into each subject file
    path="F:\\eeg\\processed\\"+pi+"\\"
    f=os.listdir(path)
    f=np.sort(f)
    
    subjectdata=pd.DataFrame()#dataframe to store subject-wise data
    
    l=len(f)
    for i in range(1,l+1):
        if(i%3==0):
            df1=pd.read_csv(path+f[i-1])#extracts files with trial information
            #some structural changes
            df1=df1.transpose()
            df1.reset_index(drop=False,inplace=True)
            df1.columns=df1.iloc[0]
            df1=df1[1:]
            df1=pd.concat([df1]*256)
            
            df2=pd.read_csv(path+f[i-3],header=None)#extracts channel data
            df2.columns=range(0,64)
            df2["timestamp"]=range(0,256)
            #merging trail and channel data
            df3=pd.concat([df1.reset_index(drop=True),df2.reset_index(drop=True)],axis=1)
            #storing each trial into subjectdata
            subjectdata=subjectdata.append(df3)
    subjectdata.to_csv(to_dir+f[0][0:11]+".csv",index=False)#storing subject-wise data as csvs
