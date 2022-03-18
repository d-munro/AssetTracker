# -*- coding: utf-8 -*-
"""

Contains all classes responsible for managing, processing, and storing information
about various assets

Created on Mon Jan  3 16:30:22 2022

Powered by CoinGecko API

@author: Dylan Munro
"""

import src.graphs.graph as graph

from typing import Final
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
import datetime

import pandas as pd

class DataManager:
    """
    Responsible for directly retrieving data from the full dataframe into the visible dataframe
    
    (Long Description TODO)
    
    Attributes:
        all_entries (pandas.DataFrame) - Full Dataframe of all asset entries loaded into the program
        visible_entries (pandas.DataFrame) - Dataframe of asset entries which are currently visible. 
            To allow for fast viewing and computation, only part of the full dataframe is loaded into view at
            one time
        tickers_to_assets (dict[string:Asset]) - 
            Dictionary mapping the ticker of an asset to its object representation
        names_to_tickers (dict[string:string]) -
            Dictionary mapping the name of an asset to its ticker
        assets_to_graphs (dict[Asset:Graph]) -
            Dictionary mapping each Asset with its current graphical representation
            
    Methods:
        
    """
    
    _REQUIRED_COLUMNS:Final = {"Ticker", "Date", "Time", "Price"}
    
    def __init__(self, all_entries):
        """
        Attributes:
            all_entries - Dataframe containing all asset entries to be loaded into program
            
        Raises:
            ValueError - If the dataframe is missing required columns
        """
        if (all_entries is not None):
            self._assets_to_graphs = None
            self._all_entries = all_entries
            self._capitalize_columns()
            self._check_column_validity()
            self._all_entries = self._all_entries.sort_values(["Ticker", "Date", "Time"])
            self._generate_percent_change()
            self._visible_entries = self._all_entries
    
    def _capitalize_columns(self):
        """
        Capitalizes all column headers for the main dataframe
        """
        capitalized_columns = []
        for column in self._all_entries.columns:
            capitalized_columns.append(column.lower().capitalize())
        self._all_entries.columns = capitalized_columns
    
    def _check_column_validity(self):
        """
        Checks if the dataframe contains required columns
        """
        required_columns_remaining = self._REQUIRED_COLUMNS
        for column in self._all_entries.columns:
            if column in self._REQUIRED_COLUMNS:
                required_columns_remaining.remove(column)
        if len(required_columns_remaining) > 0:
            raise ValueError("The spreadsheet is missing several required columns")
            
    def _generate_percent_change(self):
        """
        Generates percent change between entries of assets. If the asset changes
            between columns, then the percent change is set to 0
        """
        if "Percent Change" in self._all_entries:
            return
        self._all_entries["Percent Change"] = self._all_entries["Price"].pct_change() * 100
        
        #Change percentage errors when an asset changes
        #false_percentages = self._all_entries.ne(self._all_entries.shift()).filter(like="Ticker").apply(lambda x: x.index[x].tolist())
        false_percentages = self._all_entries["Ticker"].drop_duplicates().index.array
        for i in false_percentages:
            self._all_entries.loc[self._all_entries.index == i, "Percent Change"] = 0
            
    def hide_all_entries(self):
        """
        Hides all entries from visible dataframe
        """
        self._visible_entries = pd.DataFrame()
        
    def hide_entries(self, tickers):
        """
        Hides specified tickers from visible dataframe
        
        Attributes:
            tickers - All tickers to hide from the visible dataframe
        """
        #Tilde (~) is bitwise not operator
        for ticker in tickers:
            self._visible_entries = self._visible_entries.loc[~(self._visible_entries["Ticker"] == ticker)]
    
    def load_entries(self, tickers):
        """
        Loads all entries for chosen tickers from full dataframe into the visible dataframe
        
        Attributes:
            tickers - All entries to be loaded into the visible dataframe
            
        Raises:
            ValueError - If any tickers are not present in full dataframe
        """
        for ticker in tickers:
            try:
                new_entry = self._all_entries.loc[self._all_entries["Ticker"] == ticker]
                self._visible_entries = pd.concat([new_entry, self._visible_entries])
            except ValueError:
                message = "".join(ticker).join(" is not currently loaded. Loading entries cancelled")
                raise message             
        self._visible_entries = self._visible_entries.sort_values(["Ticker", "Date", "Time"])  
            
    def load_all_entries(self):
        """
        Loads all entries from full dataframe into visible dataframe
        """
        self._visible_entries = self._all_entries

    def get_all_tickers(self):
        """
        Returns a list of all tickers currently loaded in the visible dataframe
        """
        tickers_list = []
        tickers_df = self._all_entries["Ticker"].drop_duplicates()
        for _, ticker in tickers_df.iteritems():
            tickers_list.append(ticker)
        return tickers_list
    
    def get_visible_entries(self, tickers, starting_date = None, ending_date = None):
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
        entries_df = pd.DataFrame()
        for i in range(len(tickers)):
            ticker = tickers[i]
            new_entries = self._visible_entries.loc[self._visible_entries["Ticker"] == ticker]
            entries_df = pd.concat([entries_df, new_entries])
        if len(entries_df) == 0:
            raise UserWarning("Warning: No entries for the entered assets could be found")
        return entries_df
        
    def get_all_visible_tickers(self):
        """
        Returns a list of all tickers currently loaded in visible dataframe
        """
        assets_list = []
        assets_df = self._visible_entries["Ticker"].drop_duplicates()
        #Note: Above returns series, as a single column is returned
        for _, asset in assets_df.iteritems():
            assets_list.append(asset)
        return assets_list
            
    def get_all_visible_entries(self):
        """
        Returns all entries in the visible dataframe formatted as a list of tuples
        
        raises:
            UserWarning - if no rows are currently loaded
        """
        if len(self._visible_entries) == 0:
            raise UserWarning("No assets are currently loaded")
        return self._visible_entries
    
    def get_num_of_visible_entries(self):
        """
        Returns the number of rows in the visible dataframe
        """
        return len(self._visible_entries)
    
class Driver:
    """
    Responsible for communication between the front and back ends of the program
    """
    
    def __init__(self, df):
        self._manager = DataManager(df)
        
    #---------------------------------- Request Execution Methods--------------
    
    def _display_all_tickers(self):
        return self._manager.get_all_tickers()
    
    def _display_all_visible_tickers(self):
        if self._manager.get_num_of_visible_entries() == 0:
            raise UserWarning("There are no visible tickers")
        return self._manager.get_all_visible_tickers()
    
    def _display_visible_entries(self, request):
        return self._manager.get_visible_entries(request.get_assets())
    
    def _display_all_visible_entries(self):        
        if self._manager.get_num_of_visible_entries() == 0:
            raise UserWarning("There are no visible entries")
        return self._manager.get_all_visible_entries()
    
    def _hide_entries(self, request):
        self._manager.hide_entries(request.get_assets())
        return " ".join([", ".join(request.get_assets()), "has been removed from the view"])

    def _hide_all_entries(self):
        self._manager.hide_all_entries()
        return "All assets have been removed from view"
    
    def _load_entries(self, request):
        self._manager.load_entries(request.get_assets())
        returned_str = []
        for asset in request.get_assets():
            returned_str.append(asset)
        returned_str.append(" has been loaded into the view")
        return "".join(returned_str)
        
    def _load_all_entries(self):
        self._manager.load_all_entries()
        return "All assets have been loaded into view"
    
    def _plot_assets(self, request):
        #data = self._manager.get_visible_entries(request.get_assets)
        data = self._display_visible_entries(request)
        new_graph = graph.Graph(data)
        new_graph.plot(request.get_assets())
        return "The assets have been plotted"
    
    def _quit(self):
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
        output = ""
        choice = request.get_request()
        if choice == Request.DISPLAY_ALL_TICKERS:
            output = self._display_all_tickers()
        if choice == Request.DISPLAY_ALL_VISIBLE_TICKERS:
            output = self._display_all_visible_tickers()
        elif choice == Request.DISPLAY_VISIBLE_ENTRIES:
            output = self._display_visible_entries(request)
        elif choice == Request.DISPLAY_ALL_VISIBLE_ENTRIES:
            output = self._display_all_visible_entries()
        elif choice == Request.HIDE_ENTRIES:
            output = self._hide_entries(request)
        elif choice == Request.HIDE_ALL_ENTRIES:
            output = self._hide_all_entries()
        elif choice == Request.LOAD_ENTRIES:
            output = self._load_entries(request)
        elif choice == Request.LOAD_ALL_ENTRIES:
            output = self._load_all_entries()
        elif choice == Request.PLOT_ASSETS:
            output = self._plot_assets(request)
        elif choice == Request.QUIT:
            output = self._quit()
        return output

class Request:
    """
    Ensures that user input is syntactically correct before passing to AssetManager
    """
    
    #Request Codes
    DISPLAY_ALL_TICKERS:Final = 1 #Displays all tickers loaded in program
    DISPLAY_ALL_VISIBLE_TICKERS:Final = 2 #Displays all visible tickers
    DISPLAY_VISIBLE_ENTRIES:Final = 3 #Allows user to display only certain assets
    DISPLAY_ALL_VISIBLE_ENTRIES:Final = 4 #Displays all loaded assets
    HIDE_ENTRIES:Final = 5 #Allows user to choose which assets they wish to hide
    HIDE_ALL_ENTRIES:Final = 6 #Clears all assets from the active view
    LOAD_ENTRIES:Final = 7 #Allows user to choose which assets they wish to load
    LOAD_ALL_ENTRIES:Final = 8 #Loads all assets from spreadsheet into the active view
    PLOT_ASSETS:Final = 9 #Creates plots of an asset
    QUIT:Final = 10 #Terminate the program
    
    _SMALLEST_VALUE:Final = DISPLAY_ALL_TICKERS #Smallest int value of possible requests
    _LARGEST_VALUE:Final = QUIT #Largest int value of possible requests
    
    #dictionary of all valid requests mapped to their descriptions
    _VALID_REQUESTS:Final = {
            DISPLAY_ALL_TICKERS: "display a list of all tickers, including those hidden from view",
            DISPLAY_ALL_VISIBLE_TICKERS: "display a list of all visible tickers",
            DISPLAY_VISIBLE_ENTRIES: "display the entries of visible assets",
            DISPLAY_ALL_VISIBLE_ENTRIES: "display the entries of all visible assets",
            HIDE_ENTRIES: "hide assets from view",
            HIDE_ALL_ENTRIES: "hide all assets from view",
            LOAD_ENTRIES: "load hidden assets into view",
            LOAD_ALL_ENTRIES: "load all hidden assets into view",
            PLOT_ASSETS: "create a chart from an asset in view",
            QUIT: "terminate the program"
    }
    
    #set of all requests which can function without an asset to act upon
    _STANDALONE_REQUESTS:Final = {
        DISPLAY_ALL_TICKERS,
        DISPLAY_ALL_VISIBLE_TICKERS,
        DISPLAY_ALL_VISIBLE_ENTRIES,
        HIDE_ALL_ENTRIES,
        LOAD_ALL_ENTRIES,
        QUIT
    }
    
    
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
        if (request not in Request._STANDALONE_REQUESTS) and (assets == None):
            raise ValueError("That request requires an asset")
        self._request = request
        self._assets = assets
    
    def get_request(self):
        return self._request
    
    def get_assets(self):
        return self._assets
    
    @staticmethod
    def get_smallest_value():
        """
        Returns the smallest int that maps to a request
        """
        return Request._SMALLEST_VALUE
    
    @staticmethod
    def get_largest_value():
        """
        Returns the largest int that maps to a request
        """
        return Request._LARGEST_VALUE
        
    @staticmethod
    def get_STANDALONE_REQUESTS():
        return Request._STANDALONE_REQUESTS
    
    @staticmethod
    def get_VALID_REQUESTS():
        return Request._VALID_REQUESTS

    @staticmethod
    def is_valid_value(value):
        """
        Determines if a request value is between the smallest and largest numbers
        which map to a request
        
        Returns:
            True - If the value is between the smallest and largest request numbers
            False - If the value is not between the smallest and largest request numbers
        """
        return (value >= Request._SMALLEST_VALUE and value <= Request._LARGEST_VALUE)
        