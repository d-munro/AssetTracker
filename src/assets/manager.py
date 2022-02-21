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
        """
        Attributes:
            df - The dataframe of all data loaded into the program
            
        Raises:
            ValueError - If the dataframe is missing required columns
        """
        if (df is not None):
            self._assets_to_graphs = None
            self._df = df
            self._capitalize_columns()
            self._check_column_validity()
            self._df = self._df.sort_values(["Ticker", "Date", "Time"])
            self._visible_data = pd.DataFrame()
    
    def _capitalize_columns(self):
        """
        Capitalizes all column headers for the main dataframe
        """
        capitalized_columns = []
        for column in self._df.columns:
            capitalized_columns.append(column.lower().capitalize())
        self._df.columns = capitalized_columns
    
    def _check_column_validity(self):
        """
        Checks if the dataframe 
        """
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
        if len(entries_df) == 0:
            raise UserWarning("Warning: No action taken, {} is not present in the visible dataframe".format(ticker))
        entries = []
        for entry in entries_df.itertuples():
            entries.append(entry)
        return entries
        
    def get_visible_assets(self):
        """
        Returns a list of all assets currently loaded in the visible dataframe
        """
        assets_list = []
        assets_df = self._visible_data["Ticker"].drop_duplicates()
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
    
class Driver:
    """
    Responsible for communication between the front and back ends of the program
    """
    
    def __init__(self, df):
        self._manager = DataManager(df)
        self._visible_data = pd.DataFrame()
        
    def _execute_display_asset_names_request(self):
        pass
    
    def _execute_display_visible_assets_request(self, request):        
        if len(self._visible_data) == 0:
            raise UserWarning("There are no assets in the visible dataframe")
        assets = request.get_assets()
    
    def _execute_hide_all_assets_request(self):
        self._visible_data = pd.DataFrame(columns = self._visible_data.columns)
        return "All data in the visible dataframe has been cleared"
    
    def _execute_hide_assets_request(self, request):
        pass
    
    def _execute_load_all_assets_request(self):
        pass
    
    def _execute_load_assets_request(self, request):
        pass
    
    def _execute_plot_assets_request(self, request):
        pass
    
    def _execute_quit_request(self):
        return "Thank you for using the asset tracker"
        
    def execute_request(self, request):
        """
        Executes all user requests
        
        Attributes:
            request (Request) - The request modifying the program state
            
        Raises:
            UserWarning - If a request would not execute as expected
            
        Returns:
            String or Dataframe containing the result of the request
        """
        print("read")
        switch = {
            Request.DISPLAY_ASSET_NAMES : self._execute_display_asset_names_request(),
            Request.DISPLAY_VISIBLE_ASSETS : self._execute_display_visible_assets_request(request),
            #Request.HIDE_ALL_ASSETS : self._execute_hide_all_assets_request(),
            Request.HIDE_ASSETS : self._execute_hide_assets_request(request),
            #Request.LOAD_ALL_ASSETS : self._execute_load_all_assets_request(),
            #Request.LOAD_ASSETS : self._execute_load_assets_request(request),
            #Request.PLOT_ASSETS : self._execute_plot_asset_request(request),
            Request.QUIT : self._execute_quit_request()
        }
        try:
            return switch.get(request.get_request())
        except (UserWarning) as e:
            raise e

class Request:
    """
    Ensures that user input is syntactically correct before passing to AssetManager
    """
    
    DISPLAY_ASSET_NAMES:Final = 1
    DISPLAY_VISIBLE_ASSETS:Final = 2
    LOAD_ASSETS:Final = 3
    LOAD_ALL_ASSETS:Final = 4
    HIDE_ASSETS:Final = 5
    HIDE_ALL_ASSETS:Final = 6
    PLOT_ASSETS:Final = 7
    QUIT:Final = 8
    
    MIN_REQUEST_VALUE:Final = DISPLAY_ASSET_NAMES #Smallest int value of possible requests
    MAX_REQUEST_VALUE:Final = QUIT #Largest int value of possible requests
    
    #dictionary of all valid requests mapped to their descriptions
    _VALID_REQUESTS:Final = {
            DISPLAY_ASSET_NAMES: "display the names of all assets loaded into the program (including non-visible assets)",
            DISPLAY_VISIBLE_ASSETS: "display currently loaded visible assets",
            LOAD_ASSETS: "load assets into the visible dataframe",
            LOAD_ALL_ASSETS: "load all assets into the visible dataframe",
            HIDE_ASSETS: "hide assets currently in the visible dataframe from sight",
            HIDE_ALL_ASSETS: "hide all assets currently in the visible dataframe from sight",
            PLOT_ASSETS: "plot a chart of specified loaded assets",
            QUIT: "terminate the program"
        }
    
    #set of all requests which can function without an asset to act upon
    _REQUESTS_NO_ASSETS:Final = {DISPLAY_ASSET_NAMES, DISPLAY_VISIBLE_ASSETS,
                                  LOAD_ALL_ASSETS, HIDE_ALL_ASSETS, QUIT}
    
    
    def __init__(self, request, assets=None):
        """
        Attributes:
            request (int) - The integer representing the user request from _VALID_REQUESTS
            assets (str or list(str)) - The assets that the request is acting upon
        
        Raises:
            RequestError - If the request is not recognized
        """
        if request not in Request._VALID_REQUESTS:
            raise ValueError("Please enter the number of a valid request")
        if (request not in Request._REQUESTS_NO_ASSETS) and (assets == None):
            raise ValueError("That request requires an asset")
        self._request = request
        self._assets = assets
    
    def get_request(self):
        return self._request
    
    def get_assets(self):
        return self._assets
        
    @staticmethod
    def get_REQUESTS_NO_ASSETS():
        return Request._REQUESTS_NO_ASSETS
    
    @staticmethod
    def get_VALID_REQUESTS():
        return Request._VALID_REQUESTS
