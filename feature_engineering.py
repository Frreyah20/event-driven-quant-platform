import pandas as pd
import numpy as np

def create_features(data): # will take raw price dataframe and return feature dataframe
    df = data.copy()
    df["returns"] = df["Close"].pct_change() #pct_change = % change
    df["ma_short"] = (df["Close"].rolling(window=5).mean())
    df["ma_long"] = (df["Close"].rolling(window=20).mean())
    df["volatility"] = (df["returns"].rolling(window=20).std()) #rolling sd of returns
    df["momentum"] = (df["Close"].pct_change(periods=20))
    df["future_return"] = (df["returns"].shift(-1)) #feature today ->target tomorrow
    df["target"] = np.where(df["future_return"] > 0, 1, 0) #future_returns > 0 -> 1
    df = df.dropna()
    return df


