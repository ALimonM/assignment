import numpy as np
import argparse



def main(argv):
    X = binomial_model(float(argv.Price), float(argv.Strike), int(argv.Steps),
                       float(argv.Sigma), float(argv.Rate), float(argv.dt),argv.call_put, argv.option)
    print 'Binomial option price: $%.2f' % X[0][0]
    
def binomial_model(X0, K, N, sigma, r, delta_t, call_put, flag_americana):


    # exercise profit type
    if call_put == 'call':
        call_put = 1
    else:
        call_put = -1

    # exercise profit type
    if flag_americana == 'True':
        flag_americana = True
    else:
        flag_americana = False   

    # asset growth factor u, d
    u = np.exp(sigma* np.sqrt(delta_t))
    d = 1/u

    #asset growth probability p
    p = (np.exp(r*delta_t) - d)/(u-d)

    # Matrix of prices
    X= np.zeros((N+1, N+1))
    for i in range(0,N+1):
        for j in range(0,i+1):
            stockPrice = X0 * u**j * d**(i-j)
            X[i][j]= stockPrice
            
    exerciseProfit= X

    # Put-call exercise profit
    exerciseProfit[-1,:] = call_put * (X[-1,:]-K)   
    exerciseProfit[exerciseProfit < 0] = 0

    for i in range(N-1,-1,-1):
        for j in range(N-1,-1,-1):
            #expected profit
            e_p = (p * exerciseProfit[i+1][j+1] + (1-p)* exerciseProfit[i+1][j])/np.exp(r*delta_t)
            
            if flag_americana:
                #European
                exerciseProfit[i,j] = e_p
            else:
                # American
                exerciseProfit[i,j]= max(e_p, call_put * (X[i,j]-K))
    return exerciseProfit

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dodd-Frank html visualization.')
    parser.add_argument('-S', '--Price', help='Underlying Price', required=True)
    parser.add_argument('-K', '--Strike', help='Strike Price', required=True)
    parser.add_argument('-N', '--Steps', help='timesteps until expiration', required=True)
    parser.add_argument('-s', '--Sigma', help='risk-free discount rate', required=True)
    parser.add_argument('-r', '--Rate', help='risk-free discount rate', required=True)
    parser.add_argument('-d', '--dt', help='timestep', required=True)
    parser.add_argument('-f', '--call_put', help='timestep', required=True)
    parser.add_argument('-o', '--option', help='timestep', required=True)
    args = parser.parse_args()
    main(args)

