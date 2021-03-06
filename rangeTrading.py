# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 10:34:38 2018

@author: wgeng

"""
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import relativedelta

numTranches=3
dropPerc=0.15
profitPerc=0.1

df=pd.read_csv('./data/SPXL.csv',encoding='utf8')

#drop rows with null element
df.dropna(axis=0)

#delet Close column and change 'Adj Close' to 'Close'
del df['Adj Close']
#df=df.rename(columns={'Adj Close':'Close'})

#convert Date to DateTime format
df['Date']=pd.to_datetime(df['Date'],format='%Y-%m-%d')

#add moving averages
#roll50d=df['Close'].rolling(window=50).mean().to_frame()
#roll50d.rename(columns={'Close':'50d'},inplace=True)
#df=df.join(roll50d)

#drop rows with null element
df=df.dropna(axis=0)

#Baseline
#base = peakutils.baseline(df['50d'],10)
#peak detection
#indexes = peakutils.peak.indexes(df['50d']-base,thres=0.5,min_dist=30)
buyIdxHis=[] 
buyValHis=[]
sellIdxHis=[]
sellValHis=[]
lastPeakIdx=0
lastPeakVal=0
buyIdx=[]
buyVal=[]
sellIdx=[]
sellVal=[]
hIdx=df.columns.get_loc('High')
lIdx=df.columns.get_loc('Low')
cIdx=df.columns.get_loc('Close')
Treche1=False 
Treche2=False 
Treche3=False
for i in range(0,len(df)-1):
    if df.iloc[i,hIdx]>lastPeakVal:
        lastPeakVal=df.iloc[i,hIdx]
        lastPeakIdx=i
    if Treche3==False and (lastPeakVal-df.iloc[i,lIdx])/lastPeakVal>3*dropPerc:
        Treche3=True
        buyIdx.append(i)
        buyIdxHis.append(i)
        buyValHis.append(lastPeakVal*(1-3*dropPerc))
        buyVal.append(lastPeakVal*(1-3*dropPerc)) # buy at dropPerc
        continue
    elif Treche2==False and (lastPeakVal-df.iloc[i,lIdx])/lastPeakVal>2*dropPerc:
        Treche2=True
        buyIdx.append(i)
        buyIdxHis.append(i)
        buyValHis.append(lastPeakVal*(1-2*dropPerc))
        buyVal.append(lastPeakVal*(1-2*dropPerc)) # buy at dropPerc
        continue
    elif Treche1==False and (lastPeakVal-df.iloc[i,lIdx])/lastPeakVal>1*dropPerc:
        Treche1=True
        buyIdx.append(i)
        buyIdxHis.append(i)
        buyValHis.append(lastPeakVal*(1-1*dropPerc))
        buyVal.append(lastPeakVal*(1-1*dropPerc)) # buy at dropPerc
        #make sure not sell in the same day as buy b/c we don't know which comes first
        continue
    #sell check
    for bv in buyVal[::-1]:
        if df.iloc[i,hIdx]>=(1+profitPerc)*bv:
            sellIdxHis.append(i)
            sellValHis.append(profitPerc)
            sellIdx.append(i)
            sellVal.append(profitPerc)
            #reset Peak
            if len(buyVal)==2:
                Treche3=False
            if len(buyVal)==1:
                Treche2=False                
            if len(buyVal)==1:
                Treche1=False
                lastPeakVal=0
            #reset buyVal buyIdx
            removeIdx=buyVal.index(bv)
            buyVal.pop(removeIdx)
            buyIdx.pop(removeIdx)
print('drop Perc=%f profitPerc=%f, Total Profit=%f' %(dropPerc,profitPerc,sum(sellValHis)/3))
"""
dateIdx=df.columns.get_loc('Date')
beginDate=datetime(df.iloc[0,dateIdx])
endDate=datetime(df.ilog[-1,dateIdx])           
dateDiff = relativedelta.relativedelta(endDate, beginDate)
print('Total Profit Per Year='+sum(sellValHis)/(3*dateDiff.years))

"""
#plot
#df3=pd.DataFrame(df,columns=['Close','Adj Close'])
#df3.plot(df['Date'],figsize=(18, 14))
fig=plt.figure(figsize=(18, 14))
ax=fig.add_subplot(111)
ax.plot(df['Date'],df['Close'],color='black',marker='.')

dfBuy=df.iloc[buyIdxHis,:]
ax.plot(dfBuy['Date'],dfBuy['Close'],'r*',markersize=24)
dfSell=df.iloc[sellIdxHis,:]
ax.plot(dfSell['Date'],dfSell['Close'],'b*',markersize=24)
#ax.plot(df['Date'],roll20d,color='red',marker='.')
ax.grid(True)