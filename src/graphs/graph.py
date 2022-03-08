# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 12:45:39 2022

@author: dylmu
"""

import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

"""
Contains all methods for plotting graphs of the specified ticker
    
"""
class Graph:
    
    def __init__(self, df):
        """
        Attributes:
            df - The dataframe containing the relevant asset information
        """
        self._df = df
        
    def _generate_points(self, df, ticker):
        points = self._df.loc[self._df["Ticker"] == ticker]
        self._prices = []
        self._times = []
        for index, ticker, date, time, price in points.itertuples():
            self._prices.append(price)
            self._times.append(dt.datetime.combine(date, time))

    def plot(self, ticker):
        """
        Creates a plot of the specified asset data
        
        Attributes:
            ticker - The asset within the data set to be plotted
        """
        points = self._df.loc[self._df["Ticker"] == ticker]
        title = ticker + " price history"
        #prices = []
        #times = []
        prices = points.Price #Access price column in dataframe
        #times = dt.datetime.combine(points.Date, points.Time)
        times = pd.to_datetime(points.Date.astype(str) + ' ' + points.Time.astype(str))
        #for index, ticker, date, time, price in points.itertuples():
            #prices.append(price)
            #times.append(dt.datetime.combine(date, time))
        plt.plot_date(times, prices)
        #plt.plot(times, prices)
        plt.title(ticker + " Price History")
        plt.xlabel("Date and Time")
        plt.xticks(rotation=30, ha='right')
        plt.ylabel("Price")
        #plt.locator_params(axis="x", nbins=4)
        plt.show()
        #print(points)

        
    
