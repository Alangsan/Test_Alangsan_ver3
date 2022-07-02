import requests
import numpy as np
import calculator

#call Binance API
def binance(coin: str) -> str:
    url = f"https://api.binance.com/api/v3/avgPrice?symbol={coin}USDT"
    r = requests.get(url).json()
    if 'code' in r:
        url = f"https://api.binance.com/api/v3/avgPrice?symbol={coin}USDC"
        r = requests.get(url).json()
        if 'code' in r:
            return np.nan
        price = calculator.usdc_to_usd(r["price"])
        return price
    return r["price"]

#call CoinGecko API
def coingecko(coin: str) -> str:
    coin = coin.lower()
    search_url = f"https://api.coingecko.com/api/v3/search?query={coin}"
    r = requests.get(search_url).json()
    if r["coins"] != [] and r["coins"][0]["symbol"] == coin.upper():
        coin_id = r["coins"][0]["id"]
        price_url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        r = requests.get(price_url).json()
        return r[coin_id]["usd"]
    return np.nan

#call CoinMarketCap API
def coinmarketcap(coin: str) -> str:
    coins = ''
    for i in coin:
        coins += i+','
    coins = coins.strip(',')
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={coins}"
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '33fd2723-baa9-4ff9-815c-ab5232374a1e',
    }    
    r = requests.get(url, headers=headers).json()
    data = []
    for i in coin:
        if i == "NCASH":
            i = "NCash"
        if len(r["data"]) == 0 or r["data"][i]["total_supply"] == None:
            data.append(np.nan)
        else:
            data.append(r["data"][i]["quote"]["USD"]["price"])
    return data

#call Kraken API
def kraken(coin: str) -> str:
    r = requests.get(f"https://api.kraken.com/0/public/Ticker?pair={coin}USD").json()
    if r["error"] != []:
        return np.nan
    name = list(r["result"])[0]
    return r["result"][name]["a"][0]

##call Okex API
def okx(coin: str) -> str:
    r = requests.get(f"https://www.okex.com/api/v5/market/index-components?index={coin}-USD").json()
    if r["code"] == '0':
        for i in r["data"]["components"]:
            if i["symbol"] == f"{coin}/USD" or i["symbol"] == f"{coin}/USDT":
                return i["symPx"]
            elif i["symbol"] == f"{coin}/BTC":
                return calculator.btc_to_usd(i["symPx"])
    else:
        return np.nan

#call 5 APIs
def call_api(input_: list) -> list:
    global a
    c1 = ([float(binance(coin)) for coin in input_])
    c2 = ([float(coingecko(coin)) for coin in input_])
    c0 = (coinmarketcap(input_))
    c3 = ([float(coin) for coin in c0])
    c4 = ([float(kraken(coin)) for coin in input_])
    c5 = ([float(okx(coin)) for coin in input_])
    return np.array([c1, c2, c3, c4 ,c5])
