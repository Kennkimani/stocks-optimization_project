import requests
import pandas as pd
import time
from dotenv import load_dotenv
import os


load_dotenv()

API_KEY=os.getenv('ALPHA_VANTAGE_KEY')

tickers=['AAPL','MSFT','JPM','XOM','KO']

prices={}

for ticker in tickers:
    url='https://www.alphavantage.co/query'
    params={
        'function':'TIME_SERIES_DAILY',
        'symbol':ticker,
        'outputsize':'compact',
        'apikey':API_KEY
    }

    response=requests.get(url,params=params,timeout=30)
    result=response.json()

    if 'Time Series (Daily)' not in result:
        print(f'could not retrieve{ticker}:')
        print(result)
        continue

    stock_data=pd.DataFrame.from_dict(
        result['Time Series (Daily)'],orient='index'
    )

    stock_data.index=pd.to_datetime(stock_data.index)
    prices[ticker]=stock_data['4. close'].astype(float)

    print(f'downloded{ticker}')
    time.sleep(1)

prices_df=pd.DataFrame(prices).sort_index()
#prices_df.head()
prices_df.shape


prices_df.to_csv('stocks_data.csv')


