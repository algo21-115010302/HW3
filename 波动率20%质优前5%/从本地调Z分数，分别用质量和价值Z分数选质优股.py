# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 15:54:21 2017

@author: Yiwei Liu

Formal version1
"""
import pandas as pd
import copy
from WindPy import *
w.start();


#删去波动率前50%质优前10%

#路径
#workpath1="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/Z分数/"
#workpath2="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/用质量因子排序/质优股列表/"
#workpath3="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/用质量因子排序/质优股收盘价/"
#workpath4="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/用质量因子排序/平均收益/"
#workpath5="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/用质量因子排序/结果/"

#workpath1="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/Z分数/"
#workpath2="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/用价值因子排序/质优股列表/"
#workpath3="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/用价值因子排序/质优股收盘价/"
#workpath4="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/用价值因子排序/平均收益/"
#workpath5="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/用价值因子排序/结果/"
#
#workpath1="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/Z分数/"
#workpath2="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/所有指数等权重选股/质优股列表/"
#workpath3="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/所有指数等权重选股/质优股收盘价/"
#workpath4="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/所有指数等权重选股/平均收益/"
#workpath5="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/所有指数等权重选股/结果/"

#workpath1="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/Z分数/"
#workpath2="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/删去波动率前50%质优前10%/用质量因子排序/质优股列表/"
#workpath3="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/删去波动率前50%质优前10%/用质量因子排序/质优股收盘价/"
#workpath4="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/删去波动率前50%质优前10%/用质量因子排序/平均收益/"
#workpath5="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/删去波动率前50%质优前10%/用质量因子排序/结果/"

#workpath1="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/Z分数/"
#workpath2="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/删去波动率前50%质优前10%/用价值因子排序/质优股列表/"
#workpath3="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/删去波动率前50%质优前10%/用价值因子排序/质优股收盘价/"
#workpath4="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/删去波动率前50%质优前10%/用价值因子排序/平均收益/"
#workpath5="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/删去波动率前50%质优前10%/用价值因子排序/结果/"
#
#workpath1="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/Z分数/"
#workpath2="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/删去波动率前50%质优前10%/复合策略/质优股列表/"
#workpath3="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/删去波动率前50%质优前10%/复合策略/质优股收盘价/"
#workpath4="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/删去波动率前50%质优前10%/复合策略/平均收益/"
#workpath5="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/删去波动率前50%质优前10%/复合策略/结果/"
#
workpath1="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/Z分数/"
workpath2="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/删去波动率前50%质优前10%/所有指数等权重选股/质优股列表/"
workpath3="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/删去波动率前50%质优前10%/所有指数等权重选股/质优股收盘价/"
workpath4="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/删去波动率前50%质优前10%/所有指数等权重选股/平均收益/"
workpath5="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/删去波动率前50%质优前10%/所有指数等权重选股/结果/"

input_pct=10 
top_quality={}
dict_report={"1":"0331","2":"0630","3":"0930","4":"1231"}
dict_tddt_m={"1":"0430","2":"0831","3":"1031","4":"0430"}
last_yield=1 
return_list=[]
date_list=[]

for a in range(2010,2020):
    input_a=str(a)
    #注释掉的是用年报不用一季报的
    #for b in range(2,5):
    #现在的是5.1日调仓用一季报的    
    for b in range(1,4):  
        input_b=str(b)
        if input_a=="2019" and input_b=="2":
            break
        
        rptdate=input_a+dict_report[input_b]    #报告期（财报数据下载输入）      
        #传入参数处理，tradedate
        dict_tddt_y={"1":input_a,"2":input_a,"3":input_a,"4":str(a+1)}        
        tradedate=dict_tddt_y[input_b]+dict_tddt_m[input_b]    #报告实际发布日期（交易数据下载输入）
        #读取计算好的Z分数
        
        dfZ=pd.read_excel(workpath1+rptdate+'_Z'+'.xlsx')
        allstk=list(dfZ.index)
        dict_date={"0831":[(str(a)+"0901"),(str(a)+"1031")],"0430":[(str(a)+"0501"),(str(a)+"0831")],"1031":[(str(a)+"1101"),(str(int(a)+1)+"0430")]} 
        date_md=str(tradedate)[-4:]
        stk_vol=w.wsd(allstk, "annualstdevr_100w", dict_date[date_md][0],dict_date[date_md][0][:-2]+str(int(dict_date[date_md][0][-2:])+10), "")
        dfZ['vol_w100']=None
        for i in range(len(allstk)):   
            dfZ.iloc[i,14]=stk_vol.Data[i][0]
        
        df_vol_sort=dfZ.sort_values(by='vol_w100',ascending=True).dropna(axis=0,how='any')
        df_low_vol=df_vol_sort.iloc[:int(0.5*len(df_vol_sort)),:-1]
        
        
        #用质量因子的Z分数排序
        #df_quality_rank=df_low_vol.sort_values(by='Quality',ascending=False)
        
        #用价值因子的Z分数排序
        #df_quality_rank=df_low_vol.sort_values(by='Value',ascending=False)
        
        #用复合的Z分数排序
        #df_quality_rank=df_low_vol.sort_values(by='Sort',ascending=False)
        
        #用所有指数平均数排序
        df_low_vol["allmean"]=df_low_vol.iloc[:,:11].mean(axis=1)
        df_quality_rank=df_low_vol.sort_values(by='allmean',ascending=False)
               
        df_top_quality=df_quality_rank.iloc[0:int(len(df_quality_rank)*int(input_pct)/100)]
               
        stock_list=list(df_top_quality.index)
        pd.DataFrame(stock_list).to_excel(workpath2+rptdate+'_质优股列表'+'.xlsx',sheet_name='sheet1',index=True)
        
        price_close=w.wsd(stock_list, "close", dict_date[date_md][0],dict_date[date_md][1],"PriceAdj=F")    
        price_dict={}    
        for j in range(0,len(stock_list)):
            price_dict[stock_list[j]]=price_close.Data[j]
        df_price=pd.DataFrame(price_dict,index=price_close.Times)
        df_price.to_excel(workpath3+"Close_"+dict_date[date_md][0]+'-'+dict_date[date_md][1]+'.xlsx',sheet_name='sheet1',index=True)    
        
        df_t=pd.DataFrame()
        for m in df_price:
            df_t[m+'_yield']=df_price[m]/df_price[m][0]
        
        df_t['Col_sum'] = df_t.apply(lambda x: x.mean(), axis=1)
        df_t['Col_sum'].to_excel(workpath4+"yield_"+dict_date[date_md][0]+'-'+dict_date[date_md][1]+'.xlsx',sheet_name='sheet1',index=True)
        
        yield_li=list(df_t['Col_sum'])
        li=[x*last_yield for x in yield_li]
        last_yield=li[-1]
        return_list += li
        date_list += list(df_price.index)
                
        print(rptdate," done")


pd.DataFrame(return_list).to_excel(workpath5+"return"+'.xlsx',sheet_name='sheet1',index=True)
pd.DataFrame(date_list).to_excel(workpath5+"date"+'.xlsx',sheet_name='sheet1',index=True)

from scipy import stats
stats.ttest_rel(low,high)
stats.ttest_ind(low,high)

