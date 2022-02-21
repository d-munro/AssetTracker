# -*- coding: utf-8 -*-
"""

Contains all classes responsible for managing, processing, and storing information
about various assets

Created on Mon Jan  3 16:30:22 2022

Powered by CoinGecko API

@author: Dylan Munro
"""

from typing import Final
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
import datetime

import pandas as pd

class Request:
    """
    Ensures that user input is syntactically correct before passing to AssetManager
    """
    
    DISPLAY_ASSETS:Final = 1
    DISPLAY_VISIBLE_ASSETS:Final = 2
    LOAD_ASSET:Final = 3
    LOAD_ALL_ASSETS:Final = 4
    HIDE_ASSET:Final = 5
    HIDE_ALL_ASSETS:Final = 6
    PLOT_ASSET:Final = 7
    QUIT:Final = 8
    
    MIN_REQUEST_VALUE:Final = DISPLAY_ASSETS #Smallest int value of possible requests
    MAX_REQUEST_VALUE:Final = QUIT #Largest int value of possible requests
    
    #dictionary of all valid requests mapped to their descriptions
    _VALID_REQUESTS:Final = {
            DISPLAY_ASSETS: "display assets",
            DISPLAY_VISIBLE_ASSETS: "display currently loaded visible assets",
            LOAD_ASSET: "load an asset into the visible dataframe",
            LOAD_ALL_ASSETS: "load all assets into the visible dataframe",
            HIDE_ASSET: "hide an asset currently in the visible dataframe from sight",
            HIDE_ALL_ASSETS: "hide all assets currently in the visible dataframe from sight",
            PLOT_ASSET: "plot a chart of a loaded asset",
            QUIT: "terminate the program"
        }
    
    #set of all requests which can function without an asset to act upon
    _REQUESTS_NO_ASSETS:Final = {DISPLAY_ASSETS, DISPLAY_VISIBLE_ASSETS,
                                  LOAD_ALL_ASSETS, HIDE_ALL_ASSETS, QUIT}
    
    
    def __init__(self, request, asset=None):
        """
        Attributes:
            request - The integer representing the user request from _VALID_REQUESTS
            obj - The asset which the request is acting upon
        
        Raises:
            ValueError - If the request is not recognized
        """
        if request not in Request._VALID_REQUESTS:
            raise ValueError("Please enter the number of a valid request")
        if (request not in Request._REQUESTS_NO_ASSETS) and (asset == None):
            raise ValueError("That request requires an asset")
        self._request = request
        self._asset = asset
        self._requires_asset = not request in Request._REQUESTS_NO_ASSETS
    
    def get_request(self):
        return self._request
    
    def get_asset(self):
        return self._asset
    
    def get_requires_asset(self):
        """
        Returns true if request requires an asset to act upon
        """
        return self._requires_asset
        
    @staticmethod
    def get_REQUESTS_NO_ASSETS():
        return Request._REQUESTS_NO_ASSETS
    
    @staticmethod
    def get_VALID_REQUESTS():
        return Request._VALID_REQUESTS
    
class Driver:
    """
    Responsible for communication between the front and back ends of the program
    """
    
    def __init__(self, df):
        self._manager = DataManager(df)
        self._visible_data = pd.DataFrame()
        
    def _execute_display_asset_request(self, request):
        pass
    
    def _execute_display_visible_asset_request(self, request):
        pass
    
    def _execute_hide_all_assets_request(self, request):
        pass
    
    def _execute_hide_asset_request(self, request):
        pass
    
    def _execute_load_all_assets_request(self, request):
        pass
    
    def _execute_load_asset_request(self, request):
        pass
    
    def _execute_plot_asset_request(self, request):
        pass
    
    def _execute_quit_request(self, request):
        return "Thank you for using the asset tracker"
        
    def execute_request(self, request):
        switch = {
            Request.DISPLAY_ASSETS : self._execute_display_asset_request(request),
            Request.DISPLAY_VISIBLE_ASSETS : self._execute_display_visible_asset_request(request),
            Request.HIDE_ALL_ASSETS : self._execute_hide_all_assets_request(request),
            Request.HIDE_ASSET : self._execute_hide_asset_request(request),
            Request.LOAD_ALL_ASSETS : self._execute_load_all_assets_request(request),
            Request.LOAD_ASSET : self._execute_load_asset_request(request),
            Request.PLOT_ASSET : self._execute_plot_asset_request(request),
            Request.QUIT : self._execute_quit_request(request)
        }
        return switch.get(request.get_request())

class DataManager:
    """
    Responsible for directly retrieving data from the complete dataframe
    
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
