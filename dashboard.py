from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation , get_latest_prices
from pypfopt import risk_models
from pypfopt import expected_returns
from datetime import datetime
import streamlit as st
from yahoofinancials import YahooFinancials
import pandas as pd
import numpy as np
import os
import yfinance as yf

st.sidebar.title('Diversify')
s_date=st.sidebar.date_input('start date')
e_date=st.sidebar.date_input('end date')
a=str(s_date)
b=str(e_date)
df1 = pd.read_excel('stocks.xlsx')
df2=pd.read_excel('crypto.xlsx')
myl = df1['Names'].tolist()
myc=df2['Names'].tolist()
df = pd.DataFrame()
stock=[]
time_h = np.busday_count( s_date,e_date )
delta=e_date-s_date
time_f=delta.days
# st.write(type(time_h))
# st.write(type(time_f.days))  

if time_h>252:
    time_h=252

#x=st.sidebar.file_uploader('File uploader')
# selection=st.sidebar.selectbox('Where are you investing', ['Equity','Crypto'])

# if selection=='Equity':

option=st.sidebar.multiselect('Stocks',myl )
amount=st.sidebar.number_input('Amount to be invested',step=1000)
#amount=st.sidebar.slider('Amount to invest', min_value=100, max_value=1000000)
#amt=st.sidebar.number_input('Amount to invest', format='{:,d}')
#st.number_input(label="float displayed as integer", format="%i", value=2.4)


#st.sidebar.number_input()

#option = st.sidebar.selectbox('Which stock?',df)

# k=web.DataReader(option + '.NS', data_source='yahoo',start=s_date, end=e_date)['Adj Close']
# st.header(option)

#my_form=st.form(key="form")

def opti_ret(df,weights,amount,stock):
    abc=[]
    adj=[]
    for i in stock:
        lf=df[i].tolist()
        abc.append(lf)
    z=len(abc)-1
    #st.write(abc)
    #st.write(abc[z-1][-1])
    while z>=0:
        #st.write(abc[z][-1])
        adj.append(abc[z][-1])
        z=z-1
    c=0    
    for i in adj:
        if amount<i:
            c=c+1

    if c==len(adj):
        st.write('Add sufficient funds')
    else:
    

    
            
        mu = expected_returns.mean_historical_return(df)
        #st.write(mu)
        S = risk_models.sample_cov(df)
        #st.write(S)

        # sharpe ratio - excess return for risk involved

        ef =EfficientFrontier(mu,S)
        weights =ef.max_sharpe()
        c_weights= ef.clean_weights()
        # weights1=ef.min_volatility()
        # st.write('Vol',weights1)
        p_p=ef.portfolio_performance(verbose=True)
        st.write('Expected annual return',round((p_p[0]*100), 2))
        st.write('Annual volatility',round((p_p[1]*100), 2))
        st.write('Sharpe Ratio',p_p[2])
        latest_prices=get_latest_prices(df)
        weights= c_weights
        da = DiscreteAllocation(weights,latest_prices, total_portfolio_value= amount)
        

        alloc , leftover = da.lp_portfolio()
        

        st.write('Allocation for maximizing annual returns : ')
        st.text("")
        st.write()
        st.write(format(alloc))
        st.text("")
        st.write('Funds remaining : Rs {:.2f}'.format(leftover))



def opti_vol(df,weights,amount,stock):
    abc=[]
    adj=[]
    for i in stock:
        lf=df[i].tolist()
        abc.append(lf)
    z=len(abc)-1
    #st.write(abc)
    #st.write(abc[z-1][-1])
    while z>=0:
        #st.write(abc[z][-1])
        adj.append(abc[z][-1])
        z=z-1
    c=0    
    for i in adj:
        if amount<i:
            c=c+1

    if c==len(adj):
        st.write('Add sufficient funds')
    else:
    

    
            
        mu = expected_returns.mean_historical_return(df)
        #st.write(mu)
        S = risk_models.sample_cov(df)
        #st.write(S)

        # sharpe ratio - excess return for risk involved

        ef =EfficientFrontier(mu,S)
        weights =ef.min_volatility()
        c_weights= ef.clean_weights()
        # weights1=ef.min_volatility()
        # st.write('Vol',weights1)
        p_p=ef.portfolio_performance(verbose=True)
        st.write('Expected annual return',round((p_p[0]*100), 2))
        st.write('Annual volatility',round((p_p[1]*100), 2))
        st.write('Sharpe Ratio',p_p[2])
        latest_prices=get_latest_prices(df)
        weights= c_weights
        da = DiscreteAllocation(weights,latest_prices, total_portfolio_value= amount)
        

        alloc , leftover = da.lp_portfolio()
        

        st.write('Allocation for maximizing annual returns : ')
        st.text("")
        st.write()
        st.write(format(alloc))
        st.text("")
        st.write('Funds remaining : Rs {:.2f}'.format(leftover))



    

def variance(weights,df,time_h):
        
            

        
        st.line_chart(df)
        returns=df.pct_change()
        ca_matrix= returns.cov()*time_h
        #st.write('Matrix',ca_matrix)
        #st.write('Weights',weights)
        #var=np.dot(ca_matrix,weights)s
        is_t=np.dot(ca_matrix,weights)
        var= np.dot(weights.T,is_t)
        sd=np.sqrt(var)
        annualret=np.sum(returns.mean()*weights)*time_h
        p_var = str(round(var,2)*100)+'%'
        p_vols = str(round(sd,2)*100)+'%'
        p_annualret = str(round(annualret,2)*100)+'%'

        #with st.form("my_form1"):
        st.write('For the chosen time interval')
        st.text('')
        st.write('[Expected return : ](https://www.investopedia.com/terms/e/expectedreturn.asp)' + '  '+  p_annualret)
        st.text("")
        st.write('[Volatility/risk : ](https://www.investopedia.com/terms/v/volatility.asp) ' + '  ' + p_vols)
            #st.write('[Ann variance: ](https://www.investopedia.com/terms/v/variance.asp)'+ p_var)
            #st.write("check out this [link](https://www.investopedia.com/terms/v/variance.asp)")
            


        



            
    # except KeyError:

    #     pass
                
        
    
    
    #st.write(ca_matrix)
    #



with st.form("my_form"):
    weight=np.array([])

    for i in option:
        st.write(i)
        b=st.number_input("Portfolio % ",key=i)
        weight=np.append(weight,b)
        #st.write('Weights',weight)
        
        
        #weights=b
    #b=st.number_input("Stock quantity of ",key=i)
    
    submitted = st.form_submit_button("Submit")
    submitted1=st.form_submit_button('Diversify for maximum returns!')
    submitted2=st.form_submit_button('Diversify for minimum volatility!')


if submitted1:
    if np.sum(weight) !=1: 
        st.write('The total sum should be exactly 1.00') 


    
    else:
        if amount<=0:
            st.write('Add valid amount') 
        else:

                
    

                try:
                    for i in option:
                        stock.append(i+'.NS')

                    data = yf.download(stock,start=s_date, 
                                    end=e_date,progress=False,)['Adj Close']
                                
                        #df[i]=web.DataReader(i + '.NS', data_source='yahoo',start=s_date, end=e_date)['Adj Close']

                except KeyError or ValueError:
                    pass
                opti_ret(data,weight,amount,stock)

if submitted2:
    if np.sum(weight) !=1: 
        st.write('The total sum should be exactly 1.00') 


    
    else:
        if amount<=0:
            st.write('Add valid amount') 
        else:
            

                
    

                try:
                    for i in option:
                        stock.append(i+'.NS')

                    data = yf.download(stock,start=s_date, 
                                    end=e_date,progress=False,)['Adj Close']
                                
                        #df[i]=web.DataReader(i + '.NS', data_source='yahoo',start=s_date, end=e_date)['Adj Close']

                except KeyError or ValueError:
                    pass
                opti_vol(data,weight,amount,stock)

           



            
        
if submitted:
    if np.sum(weight) !=1: 
        st.write('The total sum should be exactly 1.00') 
    

        
    else:
        try:
            for i in option:
                stock.append(i+'.NS')

            data = yf.download(stock,start=s_date, 
                            end=e_date,progress=False,)['Adj Close']
            #st.write(data)
                        

                #df[i]=web.DataReader(i + '.NS', data_source='yahoo',start=s_date, end=e_date)['Adj Close']

        except KeyError or ValueError:

            pass
        variance(weight,data,time_h)




