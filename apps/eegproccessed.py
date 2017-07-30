# this code performs some structural changes to extract the dataset

import csv    # importing modules
import gzip
import os
import pickle
import re
import sys

from pandas import DataFrame, Series 

class EegSubject:
    #class to read,parse and store data per subject
    def __init__(self, subject_id, alcoholic, trials_data=[]):
        self.subject_id = str(subject_id)
        self.alcoholic = bool(alcoholic)
        self.trials_data = trials_data

    @staticmethod
    def from_directory(path, verbosity=1):# give path to a UCI EEG database subject folder
        
        if verbosity > 0:
            sys.stdout.write('Reading EegSubject from ' + path)
            if verbosity > 1:
                sys.stdout.write('\n')
            else:
                sys.stdout.write(':')
        m = re.match('.*/?(co\d(a|c)\d\d\d\d\d\d\d)', path)
        subject_id = m.group(1)
        alcoholic = (m.group(2)=='a')
        filenames = os.listdir(path)
        trials_data = []
        for filename in filenames:
            if verbosity > 1:
                sys.stdout.write('  reading EegTrial from ' + filename + '...')
            else:
                sys.stdout.write('.')
            try:
                trials_data.append(EegTrial.from_file(os.path.join(path, filename)))
            except Exception as e:
                sys.stdout.write('ERROR: could not read data from file: ' + str(e) + '\n')
            else:
                if verbosity > 1:
                    sys.stdout.write('SUCCESS\n')
        sys.stdout.write('\n')

        return EegSubject(subject_id=subject_id, alcoholic=alcoholic, trials_data=trials_data)

    def to_pickle(self, path='', filename=None):
        # this is used to pickle EegSubject object to disk
        
        if filename is None:
            filename = '{0.subject_id}.pkl'.format(self)
        filename = os.path.join(path, filename)
        pickle.dump(self, open(filename, 'w'), pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def from_pickle(filename):
        # reads EegSubject object from pickle file

        return pickle.load(open(filename, 'r'))

    def to_csvs(self, path=''): # give path to store the EegSubjectdata as csv
        
        subdir = os.path.join(path, self.subject_id)
        try:
            os.makedirs(subdir)
        except:
            pass
        for trial in self.trials_data:
            trial.to_csv(path=subdir)



class EegTrial:
    # this class reads, parses,and stores data per trial.

    def __init__(self, subject_id, alcoholic, trial_num, stimulus, data, channels):
        self.subject_id = str(subject_id)
        self.alcoholic = bool(alcoholic)
        self.trial_num = int(trial_num)
        self.stimulus = str(stimulus)
        self.data = DataFrame(data)
        self.channels = channels
        self.data.sort_index(inplace=True)
        self.data.sort(axis=1, inplace=True)
     
    @staticmethod
    def from_file(filename):
        #Static method to read an EegTrial object in eeg_full

        if filename.endswith('.gz'): # detects gzipped files
            f = gzip.open(filename, 'r') #opens gzipped files
        else:
            f = open(filename, 'r')
        l = f.readline()
        m = re.match('# (co\d(a|c)\d\d\d\d\d\d\d)', l) # matching the subject id
        subject_id = m.group(1)
        alcoholic = (m.group(2)=='a')
        f.readline() 
        f.readline() # skipping irrelevant lines of data
        l = f.readline()
        m = re.match('# (.*?), trial (\d+)', l) # matching stimulus and trial number
        stimulus = re.sub('\W', '', m.group(1))
        trial_num = int(m.group(2))
        # begin real data, one channel at a time
        data = dict()
        o = []
        t = []
        channels = dict()
        curr = None
        for row in csv.reader(f, delimiter=' '):
            if row[0] == '#':
                if curr is not None:
                    data[curr] = Series(data=o, index=t)
                o = []
                t = []
                assert(row[1] not in channels)
                channels[row[1]] = int(row[3])
                curr = row[1]
            else:
                assert(curr is None or curr == row[1])
                t.append(int(row[2]))
                o.append(float(row[3]))
        if curr is not None:
            data[curr] = Series(data=o, index=t)
        f.close()

        return EegTrial(subject_id=subject_id, alcoholic=alcoholic, trial_num=trial_num, stimulus=stimulus, data=DataFrame(data), channels=Series(channels))

    def get_channel_names(self):
        return list(self.data.columns)# returns data column names
    
    def get_channel_numbers(self):
        return [ self.channels[c] for c in self.data.columns ]

    def as_nparray(self):# used to turn the data into a numpy array
        
        return self.data.as_matrix()

    def to_pickle(self, path='', filename=None):#Pickles EegTrial object to disk.
       # give the path to store the pickled file

        if filename is None: # base case if file name is not given
            filename = '{0.subject_id}-{1}-{0.trial_num:03}-{0.stimulus}.pkl'.format(self, 'a' if self.alcoholic else 'c')
        filename = os.path.join(path, filename)
        pickle.dump(self, open(filename, 'w'), pickle.HIGHEST_PROTOCOL)# dumps into pickled file
        

    @staticmethod
    def from_pickle(filename):
        #Read EegTrial object from pickled file

        return pickle.load(open(filename, 'r'))

    def to_csv(self, path='', filename_base=None):
        #Store EegTrial to disk as csv files        
        #give the path neccesary to store the data into csv files
        
        if filename_base is None:# basecase when filename is not given
            filename_base = '{0.subject_id}-{1}-{0.trial_num:03}-{0.stimulus}'.format(self, 'a' if self.alcoholic else 'c')
        filename_base = os.path.join(path, filename_base)
        temp = self.data.rename(columns=self.channels).sort(axis=1).sort_index()
        temp.to_csv(filename_base + '1.csv', header=False, index=False)
        self.channels.to_csv(filename_base + '2.csv')
        f = open(filename_base + '3.csv', 'w')
        f.write('subject_id,{0.subject_id}\nalcoholic,{0.alcoholic}\ntrial_num,{0.trial_num}\nstimulus,{0.stimulus}'.format(self))
        f.close()
