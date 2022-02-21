# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 12:45:39 2022

@author: dylmu
"""

import matplotlib.pyplot as plt
import datetime as dt

"""
Contains all methods for plotting graphs of the specified ticker
    
"""
class Graph:
    
    def __init__(self, data_set):
        """
        Attributes:
            data_set - The dataframe containing the relevant asset information
        """
        self._data_set = data_set

    def plot(self, ticker):
        """
        Creates a plot of the specified asset data
        
        Attributes:
            ticker - The asset within the data set to be plotted
        """
        points = self._data_set.loc[self._data_set["Ticker"] == ticker]
        title = ticker
        prices = []
        times = []
        for index, ticker, date, time, price in points.itertuples():
            prices.append(price)
            times.append(dt.datetime.combine(date, time))
        plt.plot_date(times, prices)
        plt.title(ticker)
        plt.xlabel("Date and Time")
        plt.xticks(rotation=30, ha='right')
        plt.ylabel("Price")
        plt.locator_params(axis="x", nbins=4)
        plt.show()
        #print(points)

        
    
