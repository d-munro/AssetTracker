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

    def plot(self, tickers):
        """
        Creates a plot of the specified asset data
        
        Attributes:
            tickers - The assets within the data set to be plotted
            
        Raises:
            UserWarning - If the entered tickers are not viewable
        """
        title = " ".join(["Price history of", " vs. ".join(tickers)])
        for ticker in tickers:
            points = self._df.loc[self._df["Ticker"] == ticker]
            if len(points) == 0:
                raise UserWarning("Warning: {} was not found in the visible dataframe.\nGraphing terminated".format(ticker))
            times = pd.to_datetime(points.Date.astype(str) + ' ' + points.Time.astype(str))
            plt.plot(times, points.Price, label = ticker, marker = ".")
        
        plt.title(title)
        plt.xlabel("Date and Time")
        plt.xticks(rotation=30, ha='right')
        plt.ylabel("Price")
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.show()

        
    
