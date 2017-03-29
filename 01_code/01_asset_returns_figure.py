from yahoo_finance import Share
import numpy as np
import requests 
from scipy import stats
import plotly.plotly as py
import plotly.figure_factory as ff
import numpy as np
import plotly.offline as offline


#Input: Start and end date to compute the distribution (1 day returns)
end_date = '2017-03-20'
years= 10
start_date = str(int(end_date[:4])-years) + str(end_date[4:])

# List of 1-day returns
return_1d= []

#Yahoo api to get daily prices
yahoo = Share('^SP500TR')
stock = yahoo.get_historical(start_date,end_date )

#Compute 1 day returns 
for i in range(1,len(stock)):
    return_1d.append(float(stock[i-1]['Close'])/float(stock[i]['Close'])-1)

    
# Request to get intraday data (5 minutes tick)    
url = 'https://chartapi.finance.yahoo.com/instrument/1.0/%5ESP500TR/chartdata;type=quote;range=10d/csv'
r = requests.get(url)
intraday_prices = r.text.split('\n')[27:]

return_5m= []
last_price = 1

#Compute 5 minute returns 
for element in intraday_prices[1:-1]:
    element = element.split(',')
    return_5m.append(float(element[1])/float(last_price) -1 )
    last_price = element[1]
return_5m= return_5m[1:]

# Test of normality
print(stats.jarque_bera(return_5m))
print(stats.jarque_bera(np.array(return_1d)))


offline.init_notebook_mode(connected=True)


# Add histogram data
x1 =np.array(return_5m)
x2= np.random.normal(np.mean(x1), np.std(x1), len(x1))
# Group data together
hist_data = [x1, x2]

group_labels = ['Empirical', 'Normal']

colors = ['#3A4750', '#37AA9C']

fig = ff.create_distplot(hist_data, group_labels, show_hist=False, colors=colors)

# Add title
fig['layout'].update(title='S&P 500 Index Total Return (5 minutes)')

# Plot!
offline.iplot(fig, filename='S&P 500 Index Total Return')


