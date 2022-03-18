# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 12:45:39 2022

@author: Dylan Munro
"""

from typing import Final

import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

"""
Contains all methods for plotting graphs of the specified ticker
    
"""
class Graph:
    
    #Chart Types
    PRICE:Final = 1
    PERCENT:Final = 2
    
    def __init__(self, df):
        """
        Attributes:
            df - The dataframe containing the relevant asset information
        """
        self._df = df

    def plot(self, tickers, type = PERCENT):
        """
        Creates a plot of the specified asset data
        
        Attributes:
            tickers - The assets within the data set to be plotted
            type - Constant specifying the type of chart to be plotted
            
        Raises:
            UserWarning - If the entered tickers are not viewable
        """
        title = " ".join(["Price history of", " vs. ".join(tickers)])
        for ticker in tickers:
            points = self._df.loc[self._df["Ticker"] == ticker]
            if len(points) == 0:
                raise UserWarning("Warning: {} was not found in the visible dataframe.\nGraphing terminated".format(ticker))
            times = pd.to_datetime(points.Date.astype(str) + ' ' + points.Time.astype(str))
            
            #Determine what type of graph to plot
            if type == self.PRICE:
                plt.plot(times, points["Price"], label = ticker, marker = ".")
            elif type == self.PERCENT:
                plt.plot(times, points["Percent Change"], label = ticker, marker = ".")
        
        plt.title(title)
        plt.xlabel("Date and Time")
        plt.xticks(rotation=30, ha='right')
        
        if type == self.PRICE:
            plt.ylabel("Price")
        elif type == self.PERCENT:
            plt.ylabel("Percent Change")
        
        plt.legend(bbox_to_anchor = (1.05, 1), loc = "upper left", borderaxespad = 0)
        #Above parameters will always make legend appear in the top right corner
        #loc specifies the corner where the legend is placed
        #bbox_to_anchor specifies the location for the corner
        
        file_name = "".join([title, ".png"])
        #plt.savefig(file_name, dpi = 750, bbox_inches = "tight")
        #Must add bbox_inches so graph isn't cut off
        
        plt.show()
        #self.plot_percentage(tickers)   
