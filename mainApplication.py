'''
Created on Apr 12, 2019
Information Security project
@author: Khaled Alshatti
'''

import os
import pandas as pd
import pprint
import datetime
from tqdm import tqdm

#path to test cases
path2Files = r'C:\Khaled\Projects\Information Security\Project\Test\Excel Information Security _ Privacy Material'


#converting to human time
def convert2HumanTime(realPackets):
    Time = []
    Timestamp1 = []
    for item in realPackets:
        t= datetime.datetime.utcfromtimestamp(item/1000.0).strftime('%a,%Y-%m-%d %H:%M:%S,%p')
        timeParts = t.split(',')
        timeS = pd.to_datetime(timeParts[1],format="%Y-%m-%d %H:%M:%S",infer_datetime_format= True)
        Time.append(t)
        Timestamp1.append(timeS)
    return Time,Timestamp1

#to get the window
def getWindow(df,window):
    rangeEpoch = []
    Usage = []
    df.drop_duplicates(subset=['Real_First_Packet'],inplace=True)
    df.sort_values(by= ['Real_First_Packet'],inplace = True)
    items = df['Real_First_Packet'].values
    items = list(map(int,items))
    index = range(0,len(items))
    i=0
    limit = 0
    while (i < len(items)):
        #print('i {} , length of items {}'.format(i,len(items)))
        limit = items[i] + (window * 1000)
        Range = (df['Real_First_Packet'] >= items[i]) & (df['Real_First_Packet'] < limit)
        #print(Range)
        try:
            idx = items.index(limit)
        except:
            #val = min(items, key=lambda x:abs(x-limit))
            #idx = items.index(val)
            idx = i
        win = df[Range]
        avg = win['Internet_usage'].mean()
        rangeEpoch.append(str(items[i]))
        Usage.append(avg)
        if i == idx:
            i = idx + 1
        else:
            i=idx
    df1 = pd.DataFrame()
    df1['Starting_time'] = rangeEpoch
    df1['Average_Internet_Usage'] = Usage
    return df1
#get the month and day
def getMonthAndDay(df):
    year = []
    month = []
    day = []
    dayName = []
    for item in df['First_Time'].values:
        Parts = item.split(' ')
        Parts = Parts[0].split(',')
        dayName.append(Parts[0])
        Parts = Parts[1].split('-')
        year.append(int(Parts[0]))
        month.append(int(Parts[1]))
        day.append(int(Parts[2]))
    return year,month,day,dayName

#to get the first 2 weeks
def getFirstTwoWeeks(df):
    cond_year = df['Month'] == 2
    cond1 = df['Day'] <= 7
    cond2 = (df['Day'] > 7) & (df['Day'] <=14)
    df_week1 = df[cond_year & cond1]
    df_week2 = df[cond_year & cond2]
    return df_week1,df_week2

listOfUsers = []
#the window we are in
interval = 227

#the heart of the program. this will creat the csv file with all necessary headers and values needed 
for file in tqdm(os.listdir(path2Files)):
    if file.endswith('.xlsx'):
        print(file)
        pprint.pprint(os.path.basename(file))
        name = file.split('.')[0]
        df = pd.read_excel(path2Files + '\\' + file, sheet_name='Sheet1')
        # removing rows where Duration == 0
        mask = df['Duration'] > 0   
        df2 = df.loc[mask]   
        df2['Duration'] = df2['Duration']
        # Internet usage calcauation .                                  
        df2['Internet_usage'] = df2['doctets']/df2['Duration']          
        df2['Real_First_Packet'] = df2['Real First Packet']
        df2['Real_End_Packet'] = df2['Real End Packet']
        df2['First_Time'],df2['First_Timestamp']= convert2HumanTime(df2.Real_First_Packet)
        df3 = pd.DataFrame()
        df3['Duration'] = df2['Duration']
        df3['First_Time'] = df2['First_Time']
        df3['First_Timestamp'] = df2['First_Timestamp']
        df3['Internet_usage'] = df2['Internet_usage']
        df3['Real_First_Packet'] = df2['Real_First_Packet']
        yeardf,monthdf,daydf,dayNamedf = getMonthAndDay(df3)
        df3['Year'] = yeardf
        df3['Month'] = monthdf
        df3['Day'] = daydf
        df3['Day_Name'] = dayNamedf
        week1,week2 = getFirstTwoWeeks(df3)
        
        # Get windows
        win_df_week1 = getWindow(week1,interval)
        win_df_week2 = getWindow(week2,interval)
        
        userPath = path2Files + '\\' + os.path.basename(file)[:-5] + '\\';
        opPath =  userPath + str(interval) + '\\';

        #if the path to the output folder needed does not exist, create one
        if not os.path.exists(userPath):
            os.mkdir(userPath)
        #if the path to the output folder needed does not exist, create one
        if not os.path.exists(opPath):
            os.mkdir(opPath)

        win_df_week1.to_csv(os.path.join(path2Files + '\\' + os.path.basename(file)[:-5] + '\\' + str(interval) + '\\'+ name + '_week1.csv'))
        win_df_week2.to_csv(os.path.join(path2Files + '\\' + os.path.basename(file)[:-5] + '\\' + str(interval) + '\\'+ name + '_week2.csv'))
        week1.to_csv(path2Files + '\\' + os.path.basename(file)[:-5] + '\\' + str(interval) + '\\' + 'week1.csv',',')
        week2.to_csv(path2Files + '\\' + os.path.basename(file)[:-5] + '\\' + str(interval) + '\\' + 'week2.csv',',')
