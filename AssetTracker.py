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

class AssetManager:
    """
    Class responsible for driving back-end program execution
    
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
            self._tickers_to_assets = None
            self._assets_to_graphs = None
            self._df = df
            self._capitalize_columns()
            self._check_column_validity()
            self._df = self._df.sort_values(["Ticker", "Date", "Time"])
            #self._generate_assets()
            print(self._df)
    
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
    
    def _generate_assets(self):
        ticker, date, time, price = (
            self._df.columns.get_loc("Ticker"),
            self._df.columns.get_loc("Date"),
            self._df.columns.get_loc("Time"),
            self._df.columns.get_loc("Price")
         )
        for row in self._df.rows:
            ticker_name = self._df[ticker][date]
            price_entry = (self._df[row][date], self._df[row][time], self._df[row][price])
            if not ticker_name in self._tickers_to_assets:
                new_asset = Asset(price_entry)
                self._tickers_to_assets[ticker_name] = new_asset

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
                if (not(self.is_yes_no_response(response))):
                    raise ValueError("Please enter yes or no")
                valid_response = True
            except ValueError as e:
                print("{}".format(e))
        return response;
    
    def is_yes_no_response(self, response):
        return response.lower() == "yes" or response.lower() == "no"
    
    def load(self):
        file_loaded = False
        response = self.get_yes_no_response("Would you like to load an excel file? (Yes/No)\n")
        if response.lower() == "yes":
            while not file_loaded:
                try:
                    file_path = input("Enter the path to the file you wish to load:\n")
                    df = self.load_file(file_path)
                    self._manager = AssetManager(df)
                    file_loaded = True
                except (ValueError, FileNotFoundError) as e:
                    print("{}".format(e))
                    response = self.get_yes_no_response("Would you like to try loading a different file? (Yes/No)\n")
                    if response == "no":
                        file_loaded = True
        self.run()
    
    def load_file(self, file_path):
        """
        
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
        The main method which handles the program control flow        """
        self.load()
        self.run()
    
    def testing_main(self):
        """
        Main program used for testing
        """        
        df = pd.read_excel("Spreadsheets/functional.xlsx")
        try:
            manager = AssetManager(df)
        except ValueError as e:
            print(e)
    
    def run(self):
        pass
    
IO().testing_main()