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
workpath="C:/Users/phbs/Desktop/QMJ_CAL/"
#输入日期
#input_a=input("请输入年数（如2016）:")
#input_b=input("请输入报告期（一季报输入1,年中报输入2,三季报输入3,年报输入4）")
#input_pct=input("请输入截取质优股票百分比（如3）：")

top_quality={}

for a in range(2010,2020):
    input_a=str(a)
    #注释掉的是用年报不用一季报的
    #for b in range(2,5):
    #现在的是5.1日调仓用一季报的    
    for b in range(1,4):
        input_b=str(b)
        if input_a=="2019" and input_b=="2":
            break
        dict_report={"1":"0331","2":"0630","3":"0930","4":"1231"}
        rptdate=input_a+dict_report[input_b]    #报告期（财报数据下载输入）
            
###########可以改的###################        
        input_pct=3  #取前3%
        #传入参数处理，reportdate        

        #传入参数处理，tradedate
        dict_tddt_y={"1":input_a,"2":input_a,"3":input_a,"4":str(a+1)}
        dict_tddt_m={"1":"0430","2":"0831","3":"1031","4":"0430"}
        tradedate=dict_tddt_y[input_b]+dict_tddt_m[input_b]    #报告实际发布日期（交易数据下载输入）
        

        
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
        #word里保留删除的ast_list备查
        
        
        #%%
        
        #[]里面换成stk_list
        stks=stk_list
        
        #这里的时间是报告期（并不是出报告的日期）：年报是1231，三季报是0930，年中报是0630，一季报是0331
        #fcff企业自由现金流量,roa2_ttm2总资产报酬率,roe_ttm2净资产收益率,tot_assets资产总计,gr_ttm2营业总收入,gc_ttm2营业总成本,netprofit_ttm2归属母公司股东的净利润
        pft_ori=w.wss(stks, "fcff,roa2_ttm2,roe_ttm2,tot_assets,gr_ttm2,gc_ttm2,netprofit_ttm2","unit=1;rptDate="+rptdate+";rptType=1")

        df_ori=pd.DataFrame({'fcff':pft_ori.Data[0],'roa2_ttm2':pft_ori.Data[1],'roe_ttm2':pft_ori.Data[2],'tot_assets':pft_ori.Data[3],'gr_ttm2':pft_ori.Data[4],'gc_ttm2':pft_ori.Data[5],'netprofit_ttm2':pft_ori.Data[6]},index=stks)

#取5年前数据
        rptdate_5=str(int(input_a)-5)+dict_report[input_b]
#避免索引重复，加“_5”表示5年前数据，tot_assets资产总计,eqy_belongto_parcomsh归属母公司股东的权益,fcff企业自由现金流量,gr_ttm2营业总收入,gc_ttm2营业总成本,netprofit_ttm2归属母公司股东的净利润
        pft_ori2=w.wss(stks,"tot_assets,eqy_belongto_parcomsh,fcff,gr_ttm2,gc_ttm2,netprofit_ttm2","unit=1;rptDate="+rptdate_5+";rptType=1;currencyType=;tradeDate="+rptdate_5)
        df_ori2=pd.DataFrame({'tot_assets_5':pft_ori2.Data[0],'eqy_belongto_parcomsh_5':pft_ori2.Data[1],'fcff_5':pft_ori2.Data[2],'gr_ttm2_5':pft_ori2.Data[3],'gc_ttm2_5':pft_ori2.Data[4],'netprofit_ttm2_5':pft_ori2.Data[5]},index=stks)

#计算safety的数据，beta_100w beta(最近100周),z_score Z值,tot_liab负债合计,tot_assets资产总计
#tradeDate是beta_100w的时间，可以再在程序开头输入一个参数，改成真正调仓时的时间。
        saf_ori=w.wss(stks, "beta_100w,z_score,tot_liab,tot_assets","tradeDate="+tradedate+";rptDate="+rptdate+";unit=1;rptType=1")
        df_ori3=pd.DataFrame({"beta_100w":saf_ori.Data[0],"z_score":saf_ori.Data[1],"tot_liab":saf_ori.Data[2],"tot_assets_saf":saf_ori.Data[3]},index=stks)


#导出收益率数据
        saf_dict={}
        roe_date_li=[]
        for i in range(int(input_a)-5,int(input_a)+1):
            for j in range(1,5):
                m=str(i)+dict_report[str(j)]
                roe_date_li.append('roe_'+m)
                roe_li=w.wss(stks, "roe_ttm2","rptDate="+m)
                saf_dict['roe_'+m]=roe_li.Data[0]
                if m==rptdate:
                    break
        
        
        
        
        #计算季度ROE5年标准差的负值
        #%%
        df_ori4=pd.DataFrame(saf_dict,index=stks)
        df_ori4["vol_5y"]=list(df_ori4.std(axis=1))
        
        df_comb1=pd.merge(df_ori,df_ori2,how='inner', on=None, left_on=None, right_on=None, left_index=True,right_index=True,sort=False,suffixes=('_0', '_5'), copy=False, indicator=False)
        df_comb2=pd.merge(df_comb1,df_ori3,how='inner', on=None, left_on=None, right_on=None, left_index=True,right_index=True,sort=False, copy=False, indicator=False)
        df_comb_data=pd.merge(df_comb2,df_ori4,how='inner', on=None, left_on=None, right_on=None, left_index=True,right_index=True,sort=False, copy=False, indicator=False)
        
        df_comb_data.to_excel(workpath+rptdate+'_original_data'+'.xlsx', sheet_name='sheet1', index=True)
        
        
        
        #%%
        #profitability指标计算
        df_cal_data=pd.DataFrame()
        df_cal_data["GPOA"]=(df_comb_data["gr_ttm2"]-df_comb_data["gc_ttm2"])/df_comb_data["tot_assets"]
        df_cal_data["ROA"]=df_comb_data["roa2_ttm2"]
        df_cal_data["ROE"]=df_comb_data["roe_ttm2"]
        df_cal_data["CFOA"]=df_comb_data["fcff"]/df_comb_data["tot_assets"]
        df_cal_data["GMAR"]=(df_comb_data["gr_ttm2"]-df_comb_data["gc_ttm2"])/df_comb_data["gr_ttm2"]
        
        #growth指标计算
        df_cal_data["D_GPOA"]=((df_comb_data["gr_ttm2"]-df_comb_data["gc_ttm2"])-(df_comb_data["gr_ttm2_5"]-df_comb_data["gc_ttm2_5"]))/df_comb_data["tot_assets_5"]
        df_cal_data["D_ROA"]=(df_comb_data["netprofit_ttm2"]-df_comb_data["netprofit_ttm2_5"])/df_comb_data["tot_assets_5"]
        df_cal_data["D_ROE"]=(df_comb_data["netprofit_ttm2"]-df_comb_data["netprofit_ttm2_5"])/df_comb_data["eqy_belongto_parcomsh_5"]
        df_cal_data["D_CFOA"]=(df_comb_data["fcff"]-df_comb_data["fcff_5"])/df_comb_data["tot_assets_5"]
        df_cal_data["D_GMAR"]=((df_comb_data["gr_ttm2"]-df_comb_data["gc_ttm2"])-(df_comb_data["gr_ttm2_5"]-df_comb_data["gc_ttm2_5"]))/df_comb_data["gr_ttm2_5"]
        
        #safety指标计算
        df_cal_data["Beta_re"]=df_comb_data["beta_100w"]*(-1)
        df_cal_data["ROEVOL_re"]=df_comb_data["vol_5y"]*(-1)
        df_cal_data["Leverage_re"]=(-1)*(df_comb_data["tot_liab"]/df_comb_data["tot_assets_saf"])
        df_cal_data["ALT_Z"]=df_comb_data["z_score"]
        
        df_cal_data.to_excel(workpath+rptdate+'_cal_data'+'.xlsx', sheet_name='sheet1', index=True)



#%%记录空值，处理极端值

#在该报告期没有数据的，在排序时删除并记录数据
        df0=df_cal_data.dropna(axis=0)
        rpt_list=list(df0.index)
        unreport_stk_list=[]
        for i in stk_list:
            if i not in rpt_list:
                unreport_stk_list.append(i)
        #word里保留删除的unreport_stk_list备查


        name_li=list(df0.columns.values)
        for i in name_li:
            print(i)
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


#%%计算Z分数    
        #对每列排序并给出序号，大的编号靠前
        dfrank=df0.rank(ascending=True)
        
        #求mean&std
        mean_series=dfrank.mean()
        std_series=dfrank.std()
        
        #列索引
        index_list=list(dfrank.columns)

        #对每列Z-score标准化，保存到dfZ里
        dfZ=pd.DataFrame()
        for i in index_list:
            dfZ[i]=(dfrank[i]-mean_series[i])/std_series[i]
        
        dfZ["profitability"]=(dfZ["GPOA"]+dfZ["ROA"]+dfZ["ROE"]+dfZ["CFOA"]+dfZ["GMAR"])/5
        dfZ["growth"]=(dfZ["D_GPOA"]+dfZ["D_ROA"]+dfZ["D_ROE"]+dfZ["D_CFOA"]+dfZ["D_GMAR"])/5
        dfZ["safety"]=(dfZ["Beta_re"]+dfZ["ROEVOL_re"]+dfZ["Leverage_re"]+dfZ["ALT_Z"])/5
        
        dfZ["Quality"]=(dfZ["profitability"]+dfZ["growth"]+dfZ["safety"])/3
        
        dfZ.to_excel(workpath+rptdate+'_Z'+'.xlsx', sheet_name='sheet1', index=True)
        
        df_quality_rank=dfZ.sort_values(by='Quality',ascending=False)
        
        df_top_quality=df_quality_rank.iloc[0:int(len(stk_list)*int(input_pct)/100)]
        
        top_quality[tradedate]=[list(df_top_quality.index)]

        print(rptdate," done")

dfn=pd.DataFrame(top_quality)
dfn.to_excel(workpath+'ArrList_Industry_yjb'+'.xlsx', sheet_name='sheet1', index=True)

'''
        f1=open(workpath+rptdate+"_log.txt",'w')
        f1.write("前"+input_pct+"%质优股票：\n")
        f1.write(str(list(df_top_quality.index))+"\n")
        f1.write("总共 "+str(len(list(df_top_quality.index)))+" 支\n")
        f1.write("\n全部股票数量：\n")
        f1.write(str(len(stk_list_all))+"\n")
        f1.write("剔除垃圾股数量：\n")
        f1.write(str(len(ast_list))+"\n")
        f1.write("未发报告公司数量：\n")
        f1.write(str(len(unreport_stk_list))+"\n")
        f1.write("未发报告公司列表：\n")
        f1.write(str(unreport_stk_list)+"\n")
        f1.flush()
        f1.close()
'''

