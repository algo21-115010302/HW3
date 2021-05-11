# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 19:12:18 2018

@author: apple
"""

import pandas as pd

from WindPy import *
w.start();

workpath1="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/原始数据/"
workpath2="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/计算数据/"
workpath3="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/数据缺失筛除股/"
workpath4="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/Z分数/"
workpath5="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/选股结果/"
#传入文件是股票
df_o = pd.read_excel(workpath5+"ArrList_Industry_yjb.xlsx",sheetname="sheet1")#改成yjb
#o = pd.read_excel(workpath5+"20100930_质优股列表.xlsx",sheetname="sheet1")

last_yield=1

return_list=[]
date_list=[]

writer = pd.ExcelWriter(workpath5+'ArrList_Industry_yjb.xlsx')

#for i in range(0,len(df_o["date"])):
#for i in range(0,40):
    #a=df_o.columns[i]
    stock_li=list(df_o[str(a)])
    date_md=str(a)[-4:]
    if a<20080000:
        dict_date={"0831":[(str(a)[:4]+"0901"),(str(a+10000)[:4]+"0430")],"0430":[(str(a)[:4]+"0501"),(str(a)[:4]+"0831")]}

    else:
        dict_date={"0831":[(str(a)[:4]+"0901"),(str(a)[:4]+"1031")],"0430":[(str(a)[:4]+"0501"),(str(a)[:4]+"0831")],"1031":[(str(a)[:4]+"1101"),(str(int(a)+10000)[:4]+"0430")]} 

    #调出收盘价
    price_close=w.wsd(stock_li, "close", dict_date[date_md][0],dict_date[date_md][1],"PriceAdj=F")    
    price_dict={}    
    for j in range(0,len(stock_li)):
        price_dict[stock_li[j]]=price_close.Data[j]
    df_price=pd.DataFrame(price_dict,index=price_close.Times)
    df_price.to_excel(writer,"Ori_"+dict_date[date_md][0],index=True)
    
    
    df_t=pd.DataFrame()
    for m in df_price:
        df_t[m+'_yield']=df_price[m]/df_price[m][0]
    

    #不加权：
    df_t['Col_sum'] = df_t.apply(lambda x: x.mean(), axis=1)
    df_t.to_excel(writer,dict_date[date_md][0],index=True)
    
    yield_li=list(df_t['Col_sum'])
    li=[x*last_yield for x in yield_li]
    last_yield=li[-1]
    return_list += li
    date_list=date_list+list(df_price.index[-1])

df_fin=pd.DataFrame({"Date":date_list, "Accumulative Return":return_list})
df_fin.to_excel(workpath+"return2.xlsx",index=False)
from matplotlib.pyplot import plot

plot(date_list,return_list)
