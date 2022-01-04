# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 16:30:22 2022

@author: Dylan Munro
"""

from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
import datetime

"""
Contains all information about an asset

class variables:
    name - The full name of the asset (Ex: Apple, Bitcoin)
    ticker - The ticker for the asset (Ex: AAPL, BTC)
    type - Declares if a ticker is for a cryptocurrency or a stock
    file - The file which stores asset data if not using coingecko API
    
"""
class Asset:
    
    def __init__(self):
        pass
    
    def get_price(self, ticker: str, date: datetime.datetime()) -> float:
        pass
    
#get_price(ticker, datetime.datetime(year, month, day, hour, minute, second))

"""
Contains all methods for plotting graphs of the specified ticker

Params:
    ticker: The ticker of the stock/cryptocurrency being plotted
    
"""
class Graph:
    
    """
    params:
        asset: the Asset object containing all relevant information for the graph
    """
    def __init__(self, asset: Asset):
        pass
        
    """
    Plots the last 50 days of the closing price for the specified asset
    """
    def plot_asset(self, asset, final_date=datetime.today()):
        pass

    """
    Plots the 20 day SMA for the asset
    """
    def plot_20_day_sma(self, asset):
        pass

"""
Handles all IO requests from the user
"""
class IO:
    pass