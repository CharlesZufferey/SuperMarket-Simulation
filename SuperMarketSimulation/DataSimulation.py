# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:53:51 2020

@author: Charles
"""
#%% librairies import
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pydot
import numpy as np
import time
#%% data import
df = []
mo = 'Monday'
tu = 'Tuesday'
we = 'Wednesday'
th = 'Thursday'
fr = 'Friday'
df = pd.read_csv(r"C:\Users\Charles\Documents\Spiced\Week8\CSVDocs\monday.csv",sep=';')
df = df.append(pd.read_csv(r"C:\Users\Charles\Documents\Spiced\Week8\CSVDocs\tuesday.csv",sep=';'))
df = df.append(pd.read_csv(r"C:\Users\Charles\Documents\Spiced\Week8\CSVDocs\wednesday.csv",sep=';'))
df = df.append(pd.read_csv(r"C:\Users\Charles\Documents\Spiced\Week8\CSVDocs\thursday.csv",sep=';'))
df = df.append(pd.read_csv(r"C:\Users\Charles\Documents\Spiced\Week8\CSVDocs\friday.csv",sep=';'))
#%% data preparation and generation of probability matrix

# df_FS = order of location visited by customers
# pm = probability matrix
# df_FirstLoc = probability of visited X section as first
# df_FS1 = how many customers "entered" the shop at a given minute

df['weekday'] = pd.to_datetime(df['timestamp']).dt.weekday_name
df['UniqueID'] = df['weekday'].astype(str).str[:2]+df['customer_no'].astype(str)
df_perS = df.groupby('location')['customer_no'].count().sort_values(ascending=False)
df_perSD = df.groupby(['location','weekday'])['UniqueID'].count().sort_values(ascending=False)
df_perD = df.groupby('weekday')['customer_no'].count().sort_values(ascending=False)
df1 = df[(df['location']=='checkout')]

df_FS = df[['UniqueID','timestamp','location']]
#df_FSe = df_FS.groupby(['UniqueID']).agg({'timestamp':'min','location':'first'})
df_FS['TSNumber']=df_FS.groupby(['UniqueID']).cumcount()
df_FS = df_FS.sort_values(['UniqueID','TSNumber'])#.set_index('UniqueID')


#%%
a = []
b = []
for i in range(1,(len(df_FS['UniqueID']))):
    try:
    #print(df_FS['TSNumber'].iloc[i])
        b = []
        if df_FS['TSNumber'].iloc[i]==0:
            1==1
            #b.append(df_FS['location'].iloc[i-2])
            #b.append(df_FS['location'].iloc[i-1])
        else:
            1==1
            b.append(df_FS['location'].iloc[i-1])
            b.append(df_FS['location'].iloc[i])
            a.append(b)
    except IndexError:
        pass

dd = pd.DataFrame(a).rename(columns={0:"FirstSection",1:"SecondSection"})
df_RelationCount = pd.DataFrame(dd.groupby(['FirstSection','SecondSection']).size())
df_RelationCount = pd.DataFrame(df_RelationCount.groupby(level=0).apply(lambda x:
                                                 1 * x / (x.sum())))
c = df_RelationCount.stack().unstack().rename(columns={0:"Count"})


data = c.unstack()
pm = data
pm = pm.fillna(0)
#%% Generation of probability matrix for first location


# Generation of matrix
df_FS1 = df_FS
df_FS1['Moment'] = pd.to_datetime(df_FS1['timestamp']).dt.time
df_FS1 = df_FS1.sort_values(['UniqueID','TSNumber','Moment'])

a1 = []
b1 = []
for i in range(1,(len(df_FS1['UniqueID']))):
    try:
    #print(df_FS['TSNumber'].iloc[i])
        b1 = []
        if df_FS1['TSNumber'].iloc[i]==0:
            1==1
            #b.append(df_FS['location'].iloc[i-2])
            #b.append(df_FS['location'].iloc[i-1])
        else:
            1==1
            b1.append(df_FS1['location'].iloc[i-1])
            b1.append(df_FS1['location'].iloc[i])
            b1.append(df_FS1['Moment'].iloc[i-1])
            b1.append(df_FS1['Moment'].iloc[i])
            a1.append(b1)
    except IndexError:
        pass
dd1 = pd.DataFrame(a1).rename(columns={0:"FirstSection",1:"SecondSection",2:"ArrivalTime"
                                     ,3:"DepartureTime"})

df_FirstLoc = pd.DataFrame(dd1.groupby(['FirstSection']).size())
df_FirstLoc = pd.DataFrame(df_FirstLoc.apply(lambda x:
                                                         1*x/(x.sum())))
df_FS1=df_FS1[df_FS1['TSNumber']==0]
df_FS1['Moment'] = pd.to_datetime(df_FS1['timestamp']).dt.time
df_FS1 = df_FS1.reset_index().groupby(['Moment'])['UniqueID'].count()
#print(data)
#%%

#%% Class and function for simulation

class Simulation:
    def __init__(self,prob_FL):
        sd = []
        for i in range(len(df_FirstLoc)):
            sd.append (df_FirstLoc.iloc[i][0])
        self.initial_loc = np.random.choice(prob_FL.index,replace=True
                                          ,p=sd)
        self.p = prob_FL.loc[self.initial_loc][0]
        self.Location = [self.initial_loc]
    #def __repr__(self):
        #return f'initial loc: {self.initial_loc} with a probability of: {str(self.p)}'
        

    def mcmc2(self,prob_matrix):
        #print('initial_state: ',initial_loc)
        i= 0
        self.prob = 1
        if self.initial_loc == "dairy":
            ic = 0
        elif self.initial_loc == 'drinks':
            ic = 1
        elif self.initial_loc == 'fruit':
            ic = 2
        elif self.initial_loc == 'spices':
            ic = 3
        change = ""
        self.time1 = []
        origtime = 0
        while change != "checkout":
            #time.sleep(1)
            transname = []
            u = []
            for k in range(4):
                u = []
                for l in range(5):
                    u.append(prob_matrix.columns[l][1])
                    transname.append(u)
            #transname[ic].pop(ic)
            change = np.random.choice(transname[ic],replace=True
                                             ,p=prob_matrix.iloc[ic])
                
            if change == "checkout":
                self.prob = self.prob*prob_matrix.iloc[ic][0]
                self.Location.append(change)
                pass
            elif change == "dairy":
                self.prob = self.prob*prob_matrix.iloc[ic][1]
                self.Location.append(change)
                ic = 0
                pass
            elif change == "drinks":
                self.prob = self.prob*prob_matrix.iloc[ic][2]
                self.Location.append(change)
                ic = 1
                pass
            elif change == "fruit":
                self.prob = self.prob*prob_matrix.iloc[ic][3]
                self.Location.append(change)
                ic = 2
                pass
            elif change == "spices":
                self.prob = self.prob*prob_matrix.iloc[ic][4]
                self.Location.append(change)
                ic = 3
                pass
            origtime = origtime + 1
            self.time1.append(origtime)
        i+=1
        return self.Location
    #def __repr__(self):
        #return("Possible path: " + str(self.Location) + "\n TimeStamps:" + str(self.time1) + "\nProbability of the possible sequence of states: " + str(self.prob))
        #return str(self.Location)       
       # ...
        


#%%

#Avg time spent in each section
dd1['TimeSpentInSection'] = pd.to_datetime(dd1['DepartureTime'].astype(str)) - pd.to_datetime(dd1['ArrivalTime'].astype(str))
TimeSpent = dd1[['FirstSection','TimeSpentInSection']]
TimeSpent['TimeSpentInSection'] = pd.to_datetime(TimeSpent['TimeSpentInSection']).dt.minute
TimeSpentSection = TimeSpent.groupby(['FirstSection'])['TimeSpentInSection'].mean()

#%%Refining of the function with implementation of the avg time spent per section

# SIM = simulation results

def duration(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)

def SuperMarketSimulation(InitialProb,ProbMatrix,DFCustPerHour): #df_FirstLoc, pm, df_FS1
    MinuteEntrance = 0
    CID = 0
    TimeTracking = []
    CustomerID = []
    Location = []
    for i in  (DFCustPerHour): #every minute of the day
        AvgCust = i
        for j in range(AvgCust): #every customer per minute based on original average
            a = Simulation(InitialProb)
            a = a.mcmc2(ProbMatrix)
            #print(a)
            CID+=1
            MinuteNextLoc = 0
            for k in a:
                Location.append(k)
                TimeTracking.append(MinuteNextLoc+MinuteEntrance)
                CustomerID.append(CID)
                if k != 'checkout':
                    MinuteNextLoc+=((int(round(TimeSpentSection.loc[k]))))
                else:
                    1==1
        MinuteEntrance+=1
        MinuteNextLoc = MinuteEntrance
    df_sim1 = pd.DataFrame()
    df_sim1['Minute'] = [duration((i+420)*60) for i in  TimeTracking]
    df_sim1['CustomerID'] = CustomerID
    df_sim1['Path'] = Location
    return df_sim1
#%%
Sim = SuperMarketSimulation(df_FirstLoc,pm,df_FS1)
#%%Time spent in shop by simulated customers

df_FirstTimestamp = Sim.groupby(['CustomerID'])['Minute'].min().reset_index().set_index('CustomerID')
df_LastTimestamp = Sim.groupby(['CustomerID'])['Minute'].max().reset_index().set_index('CustomerID')
df_TimeSpent = df_FirstTimestamp.join(df_LastTimestamp,how='outer'
                                      ,lsuffix='_Arrival', rsuffix='_Departure')
df_TimeSpent['TimeSpent'] = pd.to_datetime(df_TimeSpent['Minute_Departure']) - pd.to_datetime(
        df_TimeSpent['Minute_Arrival'])
print(df_TimeSpent['TimeSpent'].describe()) # AVG Time spent 6 min 15
#%%


