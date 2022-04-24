import pandas as pd
import yfinance as yf
from yahoofinancials import YahooFinancials
import pandas_datareader as pdr


class GetData:
    def __init__(self):
        print("Get Data Created..")

    @staticmethod
    def get_data_for(script: str, start_date, end_date):
        """
        Parameters:
        ----------

        script: name of the script eg: APPL, TSLA, GOOG, etc.
        start_date, end_date: eg-'2019-01-01' and '201-06-12'
        """
        data = yf.download(
            script, start=start_date, end=end_date
        )
        return data

    @staticmethod
    def get_data_from_list(scripts, period: str = '1y', interval: str = '1d'):
        """
        Works with pandas datareader

        Parameters:
        ----------

        scripts:
            list of stocks eg,["APPL", "TSLA", "GOOG"]
        period:
            no. of years, valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        interval:
            valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        """
        print(f"Loading data for {scripts}.")
        data = yf.download(scripts, interval=interval, period=period, group_by='ticker')

        return data

    @staticmethod
    def get_data_pdr(scripts, period):
        yf.pdr_override()
        data = pdr.get_data_yahoo(scripts)
        return data
