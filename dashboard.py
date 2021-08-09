from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation , get_latest_prices
from pypfopt import risk_models
from pypfopt import expected_returns
from pandas_datareader import data as web
import matplotlib.pyplot as plt
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
myl = df1['Names'].tolist()
df = pd.DataFrame()
stock=[]
time_h = np.busday_count( s_date,e_date )
if time_h>252:
    time_h=252

#x=st.sidebar.file_uploader('File uploader')

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

def opti(df,weights,amount):
    
    mu = expected_returns.mean_historical_return(df)
    #st.write(mu)
    S = risk_models.sample_cov(df)
    #st.write(S)

    # sharpe ratio - excess return for risk involved

    ef =EfficientFrontier(mu,S)
    weights =ef.max_sharpe()
    c_weights= ef.clean_weights()
    p_p=ef.portfolio_performance(verbose=True)
    #st.write(p_p)
    latest_prices=get_latest_prices(df)
    weights= c_weights
    da = DiscreteAllocation(weights,latest_prices, total_portfolio_value= amount)
    

    alloc , leftover = da.lp_portfolio()
    

    st.write('Allocation for maximizing annual returns : ')
    st.text("")
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
    submitted1=st.form_submit_button('Diversify!')
if submitted1:
    if np.sum(weight) !=1: 
        st.write('The total sum should be exactly 1.00')  
        
    else:
        try:
            for i in option:
                stock.append(i+'.NS')

            data = yf.download(stock,start=s_date, 
                            end=e_date,progress=False,)['Adj Close']
                        
                #df[i]=web.DataReader(i + '.NS', data_source='yahoo',start=s_date, end=e_date)['Adj Close']

        except KeyError or ValueError:

            pass
        opti(data,weight,amount)
        
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
        
            
    


    












# @st.cache(allow_output_mutation=True)
# def persistdata()
#     return {}

# while b!=0:
#     with st.beta_container():
#         d = ()
#     col1, col2 = st.beta_columns(2)
#     with col1:
#          k = st.text_input("Stock",key=c2)
#     with col2:
#         v = st.number_input("Percentage",key=c3)
#     button = st.button("Add",key=c1)
#     if button:
#         if k and v:
#             d[k] = v
#     st.write(d)
#     b-=1
#     c1+=1
#     c2+=1
#     c3+=1











