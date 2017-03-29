import pandas as pd
import requests 
from bs4 import BeautifulSoup
import numpy as np
import statsmodels.api as sm


#list of technology companies with ticker
df =pd.read_csv('dataset/companylist.csv')
list_ticker = list(df['Symbol'])

ROE_stocks=[]
stocks=[]

# First 50 companies based on Market Cap 
for stock in list_ticker[:50]:
    # Webpage to scrap ROE
    url = 'https://ycharts.com/companies/'+ stock+'/return_on_equity' 
    # Request and get the info using XML structure
    soup = BeautifulSoup(requests.get(url).text)
    # Get the tables with the info
    tables = soup.find_all('table',  { "class" : "histDataTable"})
    
    # Auxiliar list for ROE by stock
    ROE_stock= []
    for table in tables:
        # td element (ROE info)
        td= table.find_all('td', { "class" : "col1"})
        td_2= table.find_all('td', { "class" : "col2"})
        for element in td_2:
            # Clean the ROE instance
            entry = element.text.replace("  ","").replace("\n","").replace("%","").replace("K","")
            # For non null ROE values
            if entry:
                ROE_stock.append(entry)
        # Filter companies with incomplete information    
        if len(ROE_stock) ==50:
            stocks.append(stock)
            ROE_stocks.append(ROE_stock)

#Some preprocessing to the lists of ROE
y= np.array([np.array(xi).astype('float') for xi in ROE_stocks])

# Compute Market ROE as the average of stock ROE 
ROE_market = range(0, y.shape[1])
for i in range(0, y.shape[1]):
    ROE_market[i] = np.average(y[:,i])

# Risk-Free Rate    
df =pd.read_csv('dataset/Treasury_q.csv')
rate = np.array(list(df['Risk Free'])[::-1])

# Excess of ROE (risk-free rate)
ROE_adjusted =np.array(ROE_market - rate)
ROE_adjusted_stock_1 = np.array(y[0,:] - rate)
ROE_adjusted_stock_2 = np.array(y[1,:] - rate)
      
# Linear regression to get the Beta for two stocks
model = sm.OLS(ROE_adjusted,ROE_adjusted_stock_1)
results = model.fit()
print(results.summary())

model = sm.OLS(ROE_adjusted,ROE_adjusted_stock_2)
results = model.fit()
print(results.summary())
