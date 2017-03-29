import pandas as pd
import numpy as np

df = pd.read_csv('dataset/EURUSD.csv')
prices = np.array(df['Bid'])

# threshold to define the directional change
dc_tres = 0.002
dc_list=[]
os_list=[]
dc_Flag=True
opt_tick = prices[0]

for i in range(1,len(prices)):
    if dc_Flag:
        if ((prices[i]/opt_tick)-1)>= dc_tres:
            if len(dc_list)>0:
                os_list.append((opt_os_tick/opt_tick)-1)
            dc_list.append((prices[i]/opt_tick)-1)
            opt_os_tick = prices[i]
            opt_tick = prices[i]
            dc_Flag = False
        elif prices[i]<opt_tick:
            opt_tick = prices[i]
        else:
            pass
    else:
        if ((prices[i]/opt_tick)-1)<= -dc_tres:
            if dc_tres:
                os_list.append((opt_os_tick/opt_tick)-1)
            dc_list.append((prices[i]/opt_tick)-1)
            opt_tick = prices[i]
            dc_Flag = True
        elif prices[i]>opt_tick:
            opt_tick = prices[i]
        else:
            pass    

print(len(dc_list))
