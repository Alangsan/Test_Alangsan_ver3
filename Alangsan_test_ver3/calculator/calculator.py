import requests
import numpy as np
import pandas as pd
import statistics

#convert bitcoin price to USD
def btc_to_usd(price: str) -> str:  
    r = requests.get(f"https://www.okex.com/api/v5/market/index-components?index=BTC-USD").json()
    for i in r["data"]["components"]:
        bitcoin_price = float(i["symPx"])
        coin_price = bitcoin_price*float(price)
        return str(coin_price)

#convert USDT price to USD
def usdt_to_usd(price: str) -> str:
    r = requests.get("https://www.okex.com/api/v5/market/index-components?index=USDT-USD").json()
    for i in r["data"]["components"]:
        usdt_price = float(i["symPx"])
        coin_price = usdt_price*float(price)
        return str(coin_price)

#convert USDC price to USD
def usdc_to_usd(price: str) -> str:
    r = requests.get("https://www.okex.com/api/v5/market/index-components?index=USDC-USD").json()
    for i in r["data"]["components"]:
        usdc_usdt = float(i["symPx"])
        usdc_price = float(usdt_to_usd(usdc_usdt))
        coin_price = usdc_price*float(price)
        return str(coin_price)

#check if error is more than 3 or not   
def detect_error(price: list) -> list:
    for col in range(np.shape(price)[1]):     #find column number
        if np.count_nonzero(pd.isna(price[:, col])) >= 3:
            price[:, col] = np.nan
    return price

#filter an outlier data
def filter_data(data: list) -> list:
    r, c = np.shape(data)
    median = np.nanmedian(data, axis=0)
    for col in range(c): 
        if median[col] is np.nan:
            continue
        for row in range(r):
            if data[row, col] is not np.nan:
                percentage = data[row, col]/median[col]*100   
                if percentage < 95 or percentage > 105:   #the data which out of the limit will be rejected 
                    data[row, col]=np.nan 
    return data

#calculate median
def cal_median(data: list) -> str:
    r, c =np.shape(data)
    price_list = []
    for col in range(c):
        if np.count_nonzero(pd.isna(data[:, col])) == 5:
            price_list.append("error")
        else:
            price_list.append(np.nanmedian(data[:, col], axis=0))
    return price_list
'''
def cal_median2(data):
    new_data = []
    for i in data:
        if i is not np.nan:
            new_data.append(float(i))
    return statistics.median(new_data)
'''        
