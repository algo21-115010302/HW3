# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 15:54:21 2017

@author: Yiwei Liu

Formal version1
"""
import pandas as pd
from WindPy import *
import copy
w.start();
#路径
workpath1="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/原始数据/"
workpath2="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/计算数据/"
workpath3="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/数据缺失筛除股/"
workpath4="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/Z分数/"
workpath5="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/选股结果/"
workpath6="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/质优股收盘价/"
workpath7="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/平均收益/"
workpath8="C:/Users/dell/Desktop/华泰实习/大成基金MSCI多因子回测/数据/结果/"

input_pct=3  #质优股取前3%
top_quality={}
dict_report={"1":"0331","2":"0630","3":"0930","4":"1231"}
dict_tddt_m={"1":"0430","2":"0831","3":"1031","4":"0430"}
last_yield=1
return_list=[]
date_list=[]

for a in range(2016,2020):
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
        
        tradedate=dict_tddt_y[input_b]+dict_tddt_m[input_b]#报告实际发布日期（交易数据下载输入）

        #取全部A股的股票代码（时点为输入日期）
        allstk=w.wset("sectorconstituent","date="+rptdate+";sector=全部A股")
        stk_list_all=allstk.Data[1]
        #取出全部st&st*等风险警示股票的股票代码（时点为输入日期）(注意这里面包含B股)
        ststk=w.wset("SectorConstituent","date="+rptdate+";sector=风险警示股票;field=wind_code,sec_name")
        stk_list_st=ststk.Data[0]
        #从全部股票中去掉st和st*股,记录删掉的st股
        stk_list=copy.deepcopy(stk_list_all)
        ast_list=[]
        for i in stk_list_all:
            if (i in stk_list_st) or (i[:3] =='300'):  #去掉垃圾股和创业板股票
                ast_list.append(i)
                stk_list.remove(i)
        #【stk_list就是要计算的股票】
        
        #[]里面换成stk_list
        stks=stk_list
        
        #这里的时间是报告期（并不是出报告的日期）：年报是1231，三季报是0930，年中报是0630，一季报是0331
        pft_ori=w.wss(stks, "roa2_ttm2,roe_ttm2,gr_ttm2,gc_ttm2,op_ttm2,eps_ttm,tot_liab,tot_assets,operatecashflow_ttm2,roic2_ttm","rptDate="+rptdate+";unit=1;rptType=1")        
        pft_ori1=w.wss(stks,"pe_ttm,pb_mrq","tradeDate="+rptdate+";unit=1;rptType=1")
        df_ori=pd.DataFrame({'roa2_ttm2':pft_ori.Data[0], #总资产报酬率（TTM）
                             'roe_ttm2':pft_ori.Data[1], #净资产收益率（TTM）
                             'gr_ttm2':pft_ori.Data[2], #营业总收入（TTM）
                             'gc_ttm2':pft_ori.Data[3], #营业总成本（TTM）
                             'op_ttm2':pft_ori.Data[4], #营业利润（TTM）
                             'eps_ttm':pft_ori.Data[5], #每股收益EPS（TTM）_PIT
                             'tot_liab':pft_ori.Data[6], #负债合计        
                             'tot_assets':pft_ori.Data[7], #资产合计
                             'operatecashflow_ttm2':pft_ori.Data[8], #经营活动现金流量（TTM）                             
                             'roic2_ttm':pft_ori.Data[9], #投入资本回报率（TTM）
                             'pe_ttm':pft_ori1.Data[0], #市盈率PE（TTM）
                             'pb_mrq':pft_ori1.Data[1]},index=stks) #市净率PB（MRQ）pft_ori=w.wss(stks, "roa2_ttm2,roe_ttm2,gr_ttm2,gc_ttm2,op_ttm2,eps_ttm,tot_liab,tot_assets,operatecashflow_ttm2,roic2_ttm","rptDate="+rptdate+";unit=1;rptType=1")

    
        #导出前三年ROE数据
        saf_dict={}
        roe_date_li=[]
        if b==1:
           m=str(a-3)+dict_report["2"]
           roe_date_li.append('roe_'+m)
           roe_li=w.wss(stks, "roe_ttm2","rptDate="+m)
           saf_dict['roe_'+m]=roe_li.Data[0]
           m=str(a-3)+dict_report["3"]
           roe_date_li.append('roe_'+m)
           roe_li=w.wss(stks, "roe_ttm2","rptDate="+m)
           saf_dict['roe_'+m]=roe_li.Data[0]
           for i in range(int(input_a)-2,int(input_a)+1):
               for j in range(1,4):
                   m=str(i)+dict_report[str(j)]
                   roe_date_li.append('roe_'+m)
                   roe_li=w.wss(stks, "roe_ttm2","rptDate="+m)
                   saf_dict['roe_'+m]=roe_li.Data[0]
                   if m==rptdate:
                      break
        if b==2:
           m=str(a-3)+dict_report["3"]
           roe_date_li.append('roe_'+m)
           roe_li=w.wss(stks, "roe_ttm2","rptDate="+m)
           saf_dict['roe_'+m]=roe_li.Data[0]
           for i in range(int(input_a)-2,int(input_a)+1):
               for j in range(1,4):
                   m=str(i)+dict_report[str(j)]
                   roe_date_li.append('roe_'+m)
                   roe_li=w.wss(stks, "roe_ttm2","rptDate="+m)
                   saf_dict['roe_'+m]=roe_li.Data[0]
                   if m==rptdate:
                      break
        if b==3:
           for i in range(int(input_a)-2,int(input_a)+1):
               for j in range(1,4):
                   m=str(i)+dict_report[str(j)]
                   roe_date_li.append('roe_'+m)
                   roe_li=w.wss(stks, "roe_ttm2","rptDate="+m)
                   saf_dict['roe_'+m]=roe_li.Data[0]
                   if m==rptdate:
                      break
            
        #计算季度ROE3年标准差       
        df_ori2=pd.DataFrame(saf_dict,index=stks)
        df_ori["roe_std_3y"]=list(df_ori2.std(axis=1))
        #保存数据        
        df_ori.to_excel(workpath1+rptdate+'_original_data'+'.xlsx', sheet_name='sheet1', index=True)
        
        #质量因子
        #盈利性
        df_cal_data=pd.DataFrame()
        df_cal_data["GPM"]=(df_ori["gr_ttm2"]-df_ori["gc_ttm2"])/df_ori["gr_ttm2"]
        df_cal_data["ROA"]=df_ori["roa2_ttm2"]
        df_cal_data["ROE"]=df_ori["roe_ttm2"]
        df_cal_data["OPR"]=df_ori["op_ttm2"]/df_ori["gr_ttm2"]
        df_cal_data["EPS"]=df_ori["eps_ttm"]
        
        #杠杆率
        df_cal_data["DTAR"]=(-1)*df_ori["tot_liab"]/df_ori["tot_assets"]
        
        #盈利稳定性
        df_cal_data["ROE_STD_3Y"]=(-1)*df_ori["roe_std_3y"]
        
        #盈利质量
        df_cal_data["OCFTGR"]=df_ori["operatecashflow_ttm2"]/df_ori["gr_ttm2"]
 
        #投资质量
        df_cal_data["ROI"]=df_ori["roic2_ttm"]
        
        #价值因子
        #TTM市盈率
        df_cal_data["PER"]=(-1)*df_ori["pe_ttm"]

        #市净率
        df_cal_data["PTBR"]=(-1)*df_ori["pb_mrq"]

        #存储数据        
        df_cal_data.to_excel(workpath2+rptdate+'_cal_data'+'.xlsx', sheet_name='sheet1', index=True)

        #记录空值，处理极端值
        #在该报告期没有数据的，在排序之前删除并记录数据
        df0=df_cal_data.dropna(axis=0)
        rpt_list=list(df0.index)
        unreport_stk_list=[]
        for i in stk_list:
            if i not in rpt_list:
                unreport_stk_list.append(i)
        usl=pd.DataFrame(unreport_stk_list)
        usl.to_excel(workpath3+rptdate+'_unreport_stocklist'+'.xlsx', sheet_name='sheet1', index=True)        
        #word里保留删除的unreport_stk_list备查

        #对财务数据添加上下界
        name_li=list(df0.columns.values)
        for i in name_li:
            data_series=df0[i]            
            md=data_series.median()
            MAD_series=abs(df0[i]-md)
            MAD=MAD_series.median()
            low_threshold=md-3*1.483*MAD
            high_threshold=md+3*1.483*MAD
            trans_li=[]
            for j in range(0,len(data_series)):
                if data_series[j]<low_threshold:
                    trans_li.append(low_threshold)
                elif data_series[j]>high_threshold:
                    trans_li.append(high_threshold)
                else:
                    trans_li.append(df0[i][j])
            df0[i]=pd.DataFrame({i:trans_li},index=df0.index.values)
        
        #计算Z分数    
        #对每列排序并给出序号，指标数值大的编号也大
        dfrank=df0.rank(ascending=True)
        
        #求mean&std
        mean_series=dfrank.mean()
        std_series=dfrank.std()
        
        #列索引
        indicator_list=list(dfrank.columns)

        #对每列Z-score标准化，保存到dfZ里
        dfZ=pd.DataFrame()
        for i in indicator_list:
            dfZ[i]=(dfrank[i]-mean_series[i])/std_series[i]
        
        dfZ["Quality"]=(dfZ["GPM"]+dfZ["ROA"]+dfZ["ROE"]+dfZ["OPR"]+
                        dfZ["EPS"]+dfZ["DTAR"]+dfZ["ROE_STD_3Y"]+
                        dfZ["OCFTGR"]+dfZ["ROI"])/9
        dfZ["Value"]=(dfZ["PER"]+dfZ["PTBR"])/2  
        
        dfZ["Sort"]=(dfZ["Quality"]+dfZ["Value"])/2
        
        dfZ.to_excel(workpath4+rptdate+'_Z'+'.xlsx', sheet_name='sheet1', index=True)
        
        df_quality_rank=dfZ.sort_values(by='Sort',ascending=False)
        
        df_top_quality=df_quality_rank.iloc[0:int(len(stk_list)*int(input_pct)/100)]
        
        dict_date={"0831":[(str(a)+"0901"),(str(a)+"1031")],"0430":[(str(a)+"0501"),(str(a)+"0831")],"1031":[(str(a)+"1101"),(str(int(a)+1)+"0430")]} 
       
        stock_list=list(df_top_quality.index)
        pd.DataFrame(stock_list).to_excel(workpath5+rptdate+'_质优股列表'+'.xlsx',sheet_name='sheet1',index=True)
        
        date_md=str(tradedate)[-4:]

        price_close=w.wsd(stock_list, "close", dict_date[date_md][0],dict_date[date_md][1],"PriceAdj=F")    
        price_dict={}    
        for j in range(0,len(stock_list)):
            price_dict[stock_list[j]]=price_close.Data[j]
        df_price=pd.DataFrame(price_dict,index=price_close.Times)
        df_price.to_excel(workpath6+"Close_"+dict_date[date_md][0]+'-'+dict_date[date_md][1]+'.xlsx',sheet_name='sheet1',index=True)    
        
        df_t=pd.DataFrame()
        for m in df_price:
            df_t[m+'_yield']=df_price[m]/df_price[m][0]
        
        df_t['Col_sum'] = df_t.apply(lambda x: x.mean(), axis=1)
        df_t['Col_sum'].to_excel(workpath7+"yield_"+dict_date[date_md][0]+'-'+dict_date[date_md][1]+'.xlsx',sheet_name='sheet1',index=True)
        
        #yield_li=list(df_t['Col_sum'])
        #li=[x*last_yield for x in yield_li]
        #last_yield=li[-1]
        #return_list += li
        #date_list += list(df_price.index)
        
       
        
        print(rptdate," done")


pd.DataFrame(return_list).to_excel(workpath8+"return"+'.xlsx',sheet_name='sheet1',index=True)
pd.DataFrame(date_list).to_excel(workpath8+"date"+'.xlsx',sheet_name='sheet1',index=True)

