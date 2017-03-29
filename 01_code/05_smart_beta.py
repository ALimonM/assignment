from yahoo_finance import Share
import numpy as np
import plotly.plotly as py
import requests 
from scipy import stats
import pandas as pd
import cvxopt as opt
from cvxopt import blas, solvers
import matplotlib.pyplot as plt


df = pd.read_csv('dataset/SP500_companies.csv')
#Input: Start and end date to compute the distribution (1 day returns)
end_date = '2016-03-20'
#Number of years to compute the Markowitz optimum
years= 5
start_date = str(int(end_date[:4])-years) + str(end_date[4:])

return_stocks= []
list_stocks = []


for element in list(df['Ticker'][:10]):
    return_1d= []

    element = element.strip()
    yahoo = Share(element)
    
    # Addres the bug of yahoo app
    try:
        stock = yahoo.get_historical(start_date,end_date )
        list_stocks.append(element)
        
        #Compute 1 day returns 
        for i in range(1,len(stock)):
            return_1d.append(float(stock[i-1]['Close'])/float(stock[i]['Close'])-1)     
        return_stocks.append(return_1d)
    except:
        pass

#compute the optimal portfolio
def optimal_portfolio(returns):
    n = len(returns)
    print(n)
    returns = np.asmatrix(returns)
    
    N = 100
    mus = [10**(5.0 * t/N - 1.0) for t in range(N)]
    
    # Convert to cvxopt matrices
    S = opt.matrix(np.cov(returns))
    pbar = opt.matrix(np.mean(returns, axis=1))
    
    # Create constraint matrices
    G = -opt.matrix(np.eye(n))   # negative n x n identity matrix
    h = opt.matrix(0.0, (n ,1))
    A = opt.matrix(1.0, (1, n))
    b = opt.matrix(1.0)
    
    # Calculate efficient frontier weights using quadratic programming
    portfolios = [solvers.qp(mu*S, -pbar, G, h, A, b)['x'] 
                  for mu in mus]
    ## CALCULATE RISKS AND RETURNS FOR FRONTIER
    returns = [blas.dot(pbar, x) for x in portfolios]
    risks = [np.sqrt(blas.dot(x, S*x)) for x in portfolios]
    ## CALCULATE THE 2ND DEGREE POLYNOMIAL OF THE FRONTIER CURVE
    m1 = np.polyfit(returns, risks, 2)
    x1 = np.sqrt(m1[2] / m1[0])
 
    # CALCULATE THE OPTIMAL PORTFOLIO
    wt = solvers.qp(opt.matrix(x1 * S), -pbar, G, h, A, b)['x']
    return np.asarray(wt), returns, risks

weights, returns, risks = optimal_portfolio(return_stocks)


# Test the portfolio
end_date = '2017-03-20'

# 1 year of information
years= 1
start_date = str(int(end_date[:4])-years) + str(end_date[4:])

return_stocks_test= []
return_stocks_1Y_test= []
return_benchmark_test =[]
return_benchmark_1Y_test=[]

# Append the benchmark index
list_stocks.append('^GSPC')


for element in list_stocks:
    return_1d= []
    element = element.strip()
    yahoo = Share(element)
    stock = yahoo.get_historical(start_date,end_date )

    
    #Compute 1 day returns, that are the inputs to compute the volatility
    for i in range(1,len(stock)):
        return_1d.append(float(stock[i-1]['Close'])/float(stock[i]['Close'])-1) 
    # Store the benchmark in other list    
    if element !='^GSPC':
        return_stocks_1Y_test.append(float(stock[0]['Close'])/float(stock[-1]['Close'])-1)
        return_stocks_test.append(return_1d)
    else:
        return_benchmark_1Y_test.append(float(stock[0]['Close'])/float(stock[-1]['Close'])-1)
        return_benchmark_test.append(return_1d)

# Compute the return and volatility of the portfolio with the Markowitz weights
port_return = np.dot(return_stocks_1Y_test, weights)
cov_matrix = np.cov(return_stocks_test)
port_vol = np.sqrt(weights.T.dot(cov_matrix).dot( weights)) * np.sqrt(260)

# Compute the return and volatility of the Benchmark
benchmark_vol = np.std(return_benchmark_test )* np.sqrt(260)
benchmark_return = return_benchmark_1Y_test[0]

print(return_stocks_1Y_test)
print(weights)

print("The 1Y return of the porfolio is " + str(np.round(port_return)))
print("The volatility (annualized) of the portfolio is " + str(np.round(port_vol)))
print("The Sharpe ratio of the porfolio is " + str(port_return/port_vol))

print("The 1Y return of the porfolio is " + str(np.round(benchmark_return*100)))
print("The volatility (annualized) of the portfolio is " + str(np.round(benchmark_vol*100)))
print("The Sharpe ratio of " + element + " is " + str(benchmark_return/benchmark_vol))
