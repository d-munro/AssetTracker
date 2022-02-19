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

"""
Contains all information about an asset

class variables:
    name - The full name of the asset (Ex: Apple, Bitcoin)
    ticker - The ticker for the asset (Ex: AAPL, BTC)
    type - Declares if a ticker is for a cryptocurrency or a stock
    
"""
class Asset:
    
    def __init__(self, *args):
        pass
    
    """
    Returns the price of the asset at a specified date
    """
    #def get_price(self, date: datetime.datetime()) -> float:
     #   pass
    
#get_price(ticker, datetime.datetime(year, month, day, hour, minute, second))

"""
Contains all methods for plotting graphs of the specified ticker
    
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
    def plot_asset(self, final_date=datetime.date.today()):
        pass

"""
Handles all IO requests from the user

class variables:
    file - The file which stores asset data if not using coingecko API
"""
class IO:
    
    #Final means static class checkers wont reassign. Must import Final from typing
    _SUPPORTED_FILES:Final = {".csv", ".xlsx"}
    
    def __init__(self):
        self._manager = None
        
    def get_file_extension(self, file_path):
        """
        
        raises:
            ValueError: If the file being loaded is not supported
        """
        file_extension = ""
        extension_index = len(file_path)
        extension_found = False
        
        #Start at end of file_path because extension is at end of file name
        for current_char in file_path[::-1]:
            if current_char == ".":
                extension_found = True
                break
            extension_index -= 1
        if not extension_found:
            raise ValueError("The file at '{}' does not have an extension".format(file_path))
        file_extension = file_path[extension_index - 1::]
        if not file_extension in self._SUPPORTED_FILES:
            raise ValueError("{} files are not supported".format(file_extension))
        return file_extension
        
    def get_yes_no_response(self, prompt):          
        valid_response = False
        while not valid_response:
            try:               
                response = input(prompt)
                if (not(response.lower() == "yes" or response.lower() == "no")):
                    raise ValueError("Please enter yes or no")
                valid_response = True
            except ValueError as e:
                print("{}".format(e))
        return response;
    
    def load(self):
        """
        Loads all preliminary data required for program operation
        """
        file_loaded = False
        response = self.get_yes_no_response("Would you like to load an excel file? (Yes/No)\n")
        if response.lower() == "yes":
            while not file_loaded:
                try:
                    file_path = input("Enter the path to the file you wish to load:\n")
                    df = self.load_file(file_path)
                    #self._manager = AssetManager(df)
                    file_loaded = True
                except (ValueError, FileNotFoundError) as e:
                    print("{}".format(e))
                    response = self.get_yes_no_response("Would you like to try loading a different file? (Yes/No)\n")
                    if response == "no":
                        file_loaded = True
        self.run()
    
    def load_file(self, file_path):
        """
        Attempts to load the file at the given filepath
        
        Attributes:
            file_path - The path to the file
        
        raises:
            ValueError: If the file being loaded is not supported
            FileNotFoundError: If the file at the file_path does not exist
        """
        file_extension = self.get_file_extension(file_path)
        try:
            if file_extension == ".xlsx" or file_extension == ".xls":
                df = pd.read_excel(file_path)
            elif file_extension == ".csv":
                df = pd.read_csv(file_path)
        except FileNotFoundError:
            raise FileNotFoundError("The file {} does not exist".format(file_path))
        return df
            
    def main(self):       
        """
        The main method which handles the program control flow
        """
        self.load()
        self.run()
    
    def data_manager_tests(self):
        """
        Method used to test the DataManager class
        """        
        df = pd.read_excel("Spreadsheets/functional.xlsx")
        try:
            manager = DataManager(df)
            #entries = manager.get_entries("BTC")
            #print("Bitcoin entries: \n{}".format(manager.load_asset("BTC")))
            #manager.get_entries("ETH")
            #print("Ethereum Entries: \n{}".format(manager.load_asset("ETH")))
            #manager.load_entries("ETH")
            #manager.load_entries("BTC")
            manager.load_all()
            print(manager.get_visible_data())
            #manager.hide_all()
            #print(manager.get_visible_data())
            manager.hide_entry("BTC", "ETH")
            #manager.delete_asset("BTC")
            print("Entries:\n")
            #print(manager.get_visible_data())
            manager.load_entries("BTC", "ETH")
            print("Entries:\n")
            print(manager.get_visible_data())
            print("Loaded assets: \n")
            self.print_list(manager.get_visible_assets())
            print("\n")
            entries = manager.get_all_entries("BTC")
            print("Entries main: {}".format(entries))
            self.print_tuples_list(entries)
            #print("Visible entries for BTC:\n{}".format(self.print_list(manager.get_all_entries("BTC"))))
        except ValueError as e:
                print(e)
    
    def print_list(self, ls):
        """
        Prints all contents in a list not containing tuples
        """
        print("Entires print: {}".format(ls))
        for item in ls:
            print("{}".format(item))
        #print("\n")
        
    def print_tuples_list(self, ls):
        for item in ls:
            index, ticker, date, time, price = item
            print("{0} {1} {2} {3}".format(ticker, date, time, price))
        
    def run(self):
        pass
    
IO().data_manager_tests()