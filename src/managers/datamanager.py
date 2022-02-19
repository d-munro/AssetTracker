# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 16:30:22 2022

Powered by CoinGecko API

@author: Dylan Munro
"""

from typing import Final
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
import datetime

import pandas as pd

class DataManager:
    """
    Executes Database Operations
    
    (Long Description TODO)
    
    Attributes:
        tickers_to_assets (dict[string:Asset]): 
            Dictionary mapping the ticker of an asset to its object representation
        names_to_tickers (dict[string:string]): 
            Dictionary mapping the name of an asset to its ticker
        assets_to_graphs (dict[Asset:Graph]): 
            Dictionary mapping each Asset with its current graphical representation
            
    Methods:
        
    """
    
    _REQUIRED_COLUMNS:Final = {"Ticker", "Date", "Time", "Price"}
    
    def __init__(self, df):
        if (df is not None):
            self._assets_to_graphs = None
            self._df = df
            self._capitalize_columns()
            self._check_column_validity()
            self._df = self._df.sort_values(["Ticker", "Date", "Time"])
            self._visible_data = pd.DataFrame()
    
    def _capitalize_columns(self):
        capitalized_columns = []
        for column in self._df.columns:
            capitalized_columns.append(column.lower().capitalize())
        self._df.columns = capitalized_columns
    
    def _check_column_validity(self):
        required_columns_remaining = self._REQUIRED_COLUMNS
        for column in self._df.columns:
            if column in self._REQUIRED_COLUMNS:
                required_columns_remaining.remove(column)
        if len(required_columns_remaining) > 0:
            raise ValueError("The spreadsheet is missing several required columns")
            
    def hide_all(self):
        """
        Hides all entries from the visible dataframe
        """
        self._visible_data = pd.DataFrame()
        
    def hide_entry(self, *tickers):
        """
        Hides specified tickers from visible database
        
        Attributes:
            tickers - All tickers to hide from the visible database
        """
        #Tilde (~) is bitwise not operator
        for ticker in tickers:
            self._visible_data = self._visible_data.loc[~(self._visible_data["Ticker"] == ticker)]
    
    def load_entries(self, *tickers):
        """
        Loads all associated tickers from the complete dataframe into the visible dataframe
        
        Attributes:
            tickers - All entries to be loaded into the visible dataframe
            
        Raises:
            ValueError - If any tickers are not present in the complete dataframe
        """
        for ticker in tickers:
            try:
                new_entry = self._df.loc[self._df["Ticker"] == ticker]
                self._visible_data = pd.concat([new_entry, self._visible_data])
            except ValueError:
                message = "".join(ticker).join(" is not currently loaded. Loading entries cancelled")
                raise message             
        self._visible_data = self._visible_data.sort_values(["Ticker", "Date", "Time"])  
            
    def load_all(self):
        """
        Loads all assets into the visible dataframe
        """
        self._visible_data = self._df

    def get_all_assets(self):
        """
        Returns a list of all assets currently loaded in the complete dataframe
        """
        assets_list = []
        assets_df = self._df["Ticker"].drop_duplicates()
        for i in range(len(assets_df)):
            assets_list.append(assets_df[i])
        return assets_list
    
    def get_all_entries(self, ticker, starting_date = None, ending_date = None):
        """
        Returns all entries in visible dataframe for a specific asset formatted
        as a list of tuples
        
        Attributes:
            ticker (string) - The name of the ticker to return entries for
            starting_date (string) - The first date that entries should be returned from in format (yyyy-mm-dd)
            ending_date (string) - The last date that entries should be returned from in format (yyyy-mm-dd)
            
        Raises:
            UserWarning - If the ticker is not loaded in the visible dataframe
        """
        entries_df = self._visible_data.loc[self._visible_data["Ticker"] == ticker]
        #print("In all entires\n{}".format(entries_df))
        if len(entries_df) == 0:
            raise UserWarning("Warning: No action taken, {} is not present in the visible dataframe".format(ticker))
        entries = []
        for entry in entries_df.itertuples():
            #print("read {}".format(entry))
            entries.append(entry)
        #print("Entries: {}".format(entries))
        return entries
        
    def get_visible_assets(self):
        """
        Returns a list of all assets currently loaded in the visible dataframe
        """
        assets_list = []
        assets_df = self._visible_data["Ticker"].drop_duplicates()
       # print("df:{}".format(assets_df))
        for i in range(len(assets_df)):
            assets_list.append(assets_df[i])
        return assets_list
            
    def get_visible_data(self):
        """
        Returns the visible dataframe
        
        raises:
            UserWarning - if no rows are currently loaded
        """
        if len(self._visible_data) == 0:
            raise UserWarning("No assets are currently loaded")
        return self._visible_data
    
#get_price(ticker, datetime.datetime(year, month, day, hour, minute, second))
