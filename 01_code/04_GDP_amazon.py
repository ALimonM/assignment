import pandas as pd
import statsmodels.api as sm
import plotly.plotly as py
import matplotlib.pyplot as plt
import numpy as np
from sklearn import  linear_model
from sklearn.metrics import r2_score

import statsmodels.api as sm
from statsmodels.formula.api import ols

from IPython.display import HTML, display


df = pd.read_csv("dataset/input_amazon.csv")
df.index = pd.DatetimeIndex(freq='Q', start= '2008-01', periods= 36)
model = ols("GDP ~ Amazon", data=df).fit()
print(model.summary())

