# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 10:12:28 2020

@author: Charles
"""

import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pydot
import numpy as np
import time
#%%
df = []
mo = 'Monday'
tu = 'Tuesday'
we = 'Wednesday'
th = 'Thursday'
fr = 'Friday'
#%%
df = pd.read_csv(r"C:\Users\Charles\Documents\Spiced\Week8\CSVDocs\monday.csv",sep=';')
df = df.append(pd.read_csv(r"C:\Users\Charles\Documents\Spiced\Week8\CSVDocs\tuesday.csv",sep=';'))
df = df.append(pd.read_csv(r"C:\Users\Charles\Documents\Spiced\Week8\CSVDocs\wednesday.csv",sep=';'))
df = df.append(pd.read_csv(r"C:\Users\Charles\Documents\Spiced\Week8\CSVDocs\thursday.csv",sep=';'))
df = df.append(pd.read_csv(r"C:\Users\Charles\Documents\Spiced\Week8\CSVDocs\friday.csv",sep=';'))
#%% Creation of new columns
df['weekday'] = pd.to_datetime(df['timestamp']).dt.weekday_name
df['UniqueID'] = df['weekday'].astype(str).str[:2]+df['customer_no'].astype(str)

#%% First analysis (customers per sections & per day Per sections)
df_perS = df.groupby('location')['customer_no'].count().sort_values(ascending=False)
df_perSD = df.groupby(['location','weekday'])['UniqueID'].count().sort_values(ascending=False)
df_perD = df.groupby('weekday')['customer_no'].count().sort_values(ascending=False)
#.sort_values(ascending=False)
#%% aggregation per location checkout (or not)
df1 = df[(df['location']=='checkout')]
df_CheckoutperT = df1.groupby(['weekday'
                              ,'timestamp'])['customer_no'].count().reset_index().set_index('timestamp')
#%%
#%% hist showing per day the # customer in checkout
df_CheckoutperT[(df_CheckoutperT['weekday']==mo)].plot(figsize = (10,10),title=mo)
df_CheckoutperT[(df_CheckoutperT['weekday']==tu)].plot(figsize = (10,10),title=tu)
df_CheckoutperT[(df_CheckoutperT['weekday']==we)].plot(figsize = (10,10),title=we)
df_CheckoutperT[(df_CheckoutperT['weekday']==th)].plot(figsize = (10,10),title=th)
df_CheckoutperT[(df_CheckoutperT['weekday']==fr)].plot(figsize = (10,10),title=fr)
#%% number of customers in each section per hour (aggregate)
df['hour']=pd.to_datetime(df['timestamp']).dt.hour
df_LocPerHour = df[['customer_no','location','hour']].groupby(['location'
                  ,'hour'])['customer_no'].count().reset_index().set_index('hour')
df_LocPerHour[(df_LocPerHour['location']=='checkout')].plot(figsize = (10,10),title='checkout')
df_LocPerHour[(df_LocPerHour['location']=='fruit')].plot(figsize = (10,10),title='fruit')
df_LocPerHour[(df_LocPerHour['location']=='dairy')].plot(figsize = (10,10),title='dairy')
df_LocPerHour[(df_LocPerHour['location']=='spices')].plot(figsize = (10,10),title='spices')
df_LocPerHour[(df_LocPerHour['location']=='drinks')].plot(figsize = (10,10),title='drinks')
#%% Time spent by customers
df_FirstTimestamp = df.groupby(['UniqueID'])['timestamp'].min().reset_index().set_index('UniqueID')
df_LastTimestamp = df.groupby(['UniqueID'])['timestamp'].max().reset_index().set_index('UniqueID')
df_TimeSpent = df_FirstTimestamp.join(df_LastTimestamp,how='outer'
                                      ,lsuffix='_Arrival', rsuffix='_Departure')
df_TimeSpent['TimeSpent'] = pd.to_datetime(df_TimeSpent['timestamp_Departure']) - pd.to_datetime(
        df_TimeSpent['timestamp_Arrival'])
print(df_TimeSpent['TimeSpent'].describe()) # AVG Time spent 6 min 15

#%% Customers present in the market over time
df['Minute'] =  pd.to_datetime(df['timestamp']).dt.time
df_Presence = df[['UniqueID','Minute']].set_index('UniqueID')
df_Presence2 = df_Presence.join(df_TimeSpent,how='left',rsuffix='_1')
df_Presence2['timestamp_Arrival'] = pd.to_datetime(df_Presence2['timestamp_Arrival']).dt.time
df_Presence2['timestamp_Departure'] = pd.to_datetime(df_Presence2['timestamp_Departure']).dt.time
df_Ts = df['Minute'].drop_duplicates()   
df_P2 = df_Presence2[['timestamp_Arrival','timestamp_Departure']].drop_duplicates()
pr = []
for i in (df_Ts):
    k = 0
    p = 0
    for j in df_P2.index:
        if (i >= df_P2.iloc[k,0] and i <= df_P2.iloc[k,1]):
            p=p+1
        else:
            1==1
        k=k+1
    pr.append(p)
df_Ts = pd.DataFrame(df_Ts)
df_Ts['CountCustomers'] = pr        
df_Ts1 = df_Ts
df_Ts = df_Ts.set_index('Minute')
df_Ts = df_Ts.sort_index()
df_Ts.plot()       
#%% First, second and following section visited by each customers
df_FS = df[['UniqueID','timestamp','location']]
df_FS1 = df_FS.groupby(['UniqueID']).agg({'timestamp':'min','location':'first'})
df_SS = df_FS
df_SS['TSNumber']=df_FS.groupby(['UniqueID']).cumcount()
df_SS = df_SS[(df_SS['TSNumber']==1)].set_index('UniqueID')
df_FandSSection = df_FS1.join(df_SS,how='left',rsuffix='_1')
#%% FS = First Section / FollowingS + Following sections
df_FollowingS = df_FS
df_FollowingS['TSNumber']=df_FS.groupby(['UniqueID']).cumcount()
df_FollowingS= df_FollowingS[(df_FollowingS['TSNumber']==2)].set_index('UniqueID')
df_FollowingS2 = df_FS
df_FollowingS2['TSNumber']=df_FS.groupby(['UniqueID']).cumcount()
df_FollowingS2= df_FollowingS2[(df_FollowingS2['TSNumber']==3)].set_index('UniqueID')
#%%
df_MoreSection = df_FandSSection.join(df_FollowingS,how='left',rsuffix='_2')
df_MoreSection = df_MoreSection.join(df_FollowingS2,how='left',rsuffix='_3')
#%%
ct = pd.crosstab(df_MoreSection['location'], [df_MoreSection['location_1'],df_MoreSection['location_2']]
, rownames=['location'], colnames=['location_1', 'location_2'])
ct2 = pd.crosstab(df_MoreSection['location'], [df_MoreSection['location_1']]
, rownames=['location'], colnames=['location_1'])
#%%
ct2.plot.bar()
#%%Plots showing distribution of first vs following visits
df_FS1.reset_index().groupby(['location'])['UniqueID'].count().plot.bar(title='First visited section')
#%%
df_AllFollowingS = df_FS
df_AllFollowingS['TSNumber']=df_FS.groupby(['UniqueID']).cumcount()
df_AllFollowingS= df_AllFollowingS[(df_AllFollowingS['TSNumber']>0)]
df_AllFollowingS.groupby(['location'])['UniqueID'].count().plot.bar(title='Following sections')
#%% Price per customer, if all customers that go to a section only take one item of this section per visit
df_History = df
price = []
for i in df['location']:
    if i == 'fruit':
        price.append(4)
    elif i == 'spices':
        price.append(3)
    elif i == 'drinks':
        price.append(6)
    elif i == 'dairy':
        price.append(5)
    else:
        price.append(0)
df_History['price']=price
df_PricePerCustomer = df_History.groupby(['UniqueID'])['price'].sum().sort_values(ascending=False)
#%% Money made per location based on the number of visits
df_PricePerLoc = df_History.groupby(['location']).agg({'UniqueID' : 'count'
                                   , 'price':'sum'}).rename(columns={'UniqueID':'NbVisits'
                                                  ,'price':'TotalPrice'}).plot.bar()
#%% all location connections
df_FS = df_FS.sort_values(['UniqueID','TSNumber'])
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

#%%
dd = pd.DataFrame(a).rename(columns={0:"FirstSection",1:"SecondSection"})
df_RelationCount = pd.DataFrame(dd.groupby(['FirstSection','SecondSection']).size())
df_RelationCount = pd.DataFrame(df_RelationCount.groupby(level=0).apply(lambda x:
                                                 1 * x / (x.sum())))
df_FirstLoc = pd.DataFrame(df_FS1.groupby(['location']).size())
df_FirstLoc = pd.DataFrame(df_FirstLoc.apply(lambda x:
                                                         1*x/(x.sum())))
c = df_RelationCount.stack().unstack().rename(columns={0:"Count"})



#%%
graph = pydot.Dot(graph_type='digraph')

for i in range(len(c.index)):
    edge = pydot.Edge(c.index[i][0],c.index[i][1])
    # and we obviosuly need to add the edge to our graph
    graph.add_edge(edge)
    edge.set_label(str(c['Count'][i])+"%")
    edge.set_color('#AEF359' if c['Count'][i] < 20 else '#03C04A' if c['Count'][i] < 40 else '#32612D')
    edge.set_penwidth(1 if c['Count'][i] < 20 else 3 if c['Count'][i] < 40 else 5)        

graph.write_png(r'C:\Users\Charles\Documents\Spiced\Week8\ProbNextLocation.png') 

#%%

data = c.unstack()
print(data)



#%%Probability matrix: pm
pm = data
pm = pm.fillna(0)
#pm = pm.replace(2.72,2.71)
#%%
transname = []
u = []
for k in range(4):
    u = []
    for l in range(5):
        u.append(pm.columns[l][1])
    transname.append(u)
transmatrix = []
t = []
for i in range(4):
    t=[]
    for j in range(5):
        t.append(pm.iloc[i,j])
    transmatrix.append(t)
#%%
print(transname[1].pop(1))
print(transname)
#%%
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
        CurrentState = self.initial_loc
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
        
    def __repr__(self):
        #return("Possible path: " + str(self.Location) + "\n TimeStamps:" + str(self.time1) + "\nProbability of the possible sequence of states: " + str(self.prob))
        #return str(self.Location)       
        ...
        
    def AllDaySim(self):  
        Minute = 0
        CID = 0
        TimeTracking = []
        CustomerID = []
        Location = []
        for i in  (df_FS1):
            AvgCust = i
            for j in range(AvgCust):
                a = Simulation(df_FirstLoc)
                a.mcmc2(pm)
                #print(a)
                CID+=1
                TimeTracking.append(Minute)
                CustomerID.append(CID)
                Location.append(a)
                
            Minute+=1
        df_sim2 = pd.DataFrame()
        df_sim2['Minute'] = TimeTracking
        df_sim2['CustomerID'] = CustomerID
        df_sim2['Path'] = Location
#%%
df_FS1['Moment'] = pd.to_datetime(df_FS1['timestamp']).dt.time
df_FS1 = df_FS1.reset_index().groupby(['Moment'])['UniqueID'].count()
#%%
Minute = 0
CID = 0
TimeTracking = []
CustomerID = []
Location = []
for i in  (df_FS1):
    AvgCust = i
    for j in range(AvgCust):
        a = Simulation(df_FirstLoc)
        a.mcmc2(pm)
        print(a)
        CID+=1
        TimeTracking.append(Minute)
        CustomerID.append(CID)
        Location.append(a)
        
    Minute+=1
df_sim = pd.DataFrame()
df_sim['Minute'] = TimeTracking
df_sim['CustomerID'] = CustomerID
df_sim['Path'] = Location    
    
    
#%%
#%%
a = Simulation(df_FirstLoc)
a.mcmc2(pm)
a.AllDaySim()

    