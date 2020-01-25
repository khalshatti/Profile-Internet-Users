'''
Created on Apr 12, 2019

@author: Khaled
'''

import scipy.stats
import os
import pandas as pd
import math
import pprint

inPath  = r'C:\Khaled\Projects\Information Security\Project\Test\Application Output' 
outPath = r'C:\Khaled\Projects\Information Security\Project\PIUOUT\AA PIU output'

l = os.listdir(inPath)

#window = [10, 227, 300]

#calculated the spearman's Correlation
def calcSpear(la, lb, length):
    if(len(la) > len(lb)):
        return scipy.stats.spearmanr(la[0 : length], lb[0 : length])[0]
    else:
        return scipy.stats.spearmanr(la[0 : length], lb[0 : length])[0]

#calculated z value
def calcZ(r1a2a, r1a2b, r2a2b, N):

    rm2 = ((r1a2a ** 2) + (r1a2b ** 2)) / 2
    f = (1 - r2a2b) / (2 * (1 - rm2))
    h = (1 - (f * rm2)) / (1 - rm2)

    z1a2a = 0.5 * (math.log10((1 + r1a2a)/(1 - r1a2a)))
    z1a2b = 0.5 * (math.log10((1 + r1a2b)/(1 - r1a2b)))

    z = (z1a2a - z1a2b) * (math.sqrt(N-3)) / (2 * (1 - r2a2b) * h)

    return z

#Calculate p value
def calcP(z):
    p = 0.3275911
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429

    sign = None
    if z < 0.01:
        sign = -1
    else:
        sign = 1

    x = abs(z) / (2 ** 0.5)
    t = 1 / (1 + p * x)
    erf = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)

    return 0.5 * (1 + sign * erf)

#time windows
window = [10, 227, 300]

i = 0
#the heart of the calculations. this is where we place the values into a  CSV file
for win in window:
    print("----hello----",win)
    biglist = []
    i = 0
    j = 0
    while(i < len(l)):
        lst = []
        dfa_week1 = pd.read_csv(inPath + '\\' + os.path.basename(l[i]) + '\\' + str(win) + '\\week1.csv')
        dfa_week2 = pd.read_csv(inPath + '\\' + os.path.basename(l[i]) + '\\' + str(win) + '\\week2.csv')
        j = i + 1
        while(j < len(l)):
            dfb_week1 = pd.read_csv(inPath + '\\' + os.path.basename(l[j]) + '\\' + str(win) + '\\week1.csv')
            dfb_week2  = pd.read_csv(inPath + '\\' + os.path.basename(l[j]) + '\\' + str(win) + '\\week2.csv')

            #takes the value of internet usage
            l1a = dfa_week1['Internet_usage'].values.tolist()
            l2a = dfa_week2['Internet_usage'].values.tolist()
            l2b = dfb_week2['Internet_usage'].values.tolist()

            length  = min(len(l1a), len(l2a), len(l2b))
            #caculates the r1a2a, r1a2b, r2a2b
            r1a2a = calcSpear(l1a, l2a, length)
            r1a2b = calcSpear(l1a, l2b, length)
            r2a2b = calcSpear(l2a, l2b, length)

            if(length > 3):
                z = calcZ(r1a2a, r1a2b, r2a2b, length)
            else :
                z = calcZ(r1a2a, r1a2b, r2a2b, 3)

            p = calcP(z)
            
            #push value p in list
            lst.append(p)
            j = j + 1
            print ('j=',j)

        flist = ['x'] * (54-len(lst)) + lst
        pprint.pprint(flist)
        biglist.append(flist)
        print('i=',i)
        i = i + 1

    #print the output into a csv
    df_final = pd.DataFrame(biglist)
    df_final.to_csv(outPath + '\\' + str(win) + '.csv')





