# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 10:02:19 2022

@author: dylmu
"""

import src.assets.manager as dm
import src.graphs.graph

import pandas as pd

def data_manager_tests():
    """
    Function used to test the DataManager class
    """        
    df = pd.read_excel("resources/spreadsheets/functional.xlsx")
    try:
        manager = dm.DataManager(df)
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
        print_list(manager.get_visible_assets())
        print("\n")
        entries = manager.get_all_entries("BTC")
        print("Entries main: {}".format(entries))
        print_tuples_list(entries)
        #print("Visible entries for BTC:\n{}".format(self.print_list(manager.get_all_entries("BTC"))))
    except ValueError as e:
        print(e)
        
def graph_tests():
    """
    Function used to test graph functionality
    """
    df = pd.read_excel("resources/spreadsheets/functional.xlsx")
    try:
        manager = dm.DataManager(df)
        manager.load_all()
        graph = src.graphs.graph.Graph(manager.get_visible_data())
        graph.plot("BTC")
    except ValueError as e:
        print(e)
    
def print_list(ls):
    """
    Prints all contents in a list not containing tuples
    """
    print("Entires print: {}".format(ls))
    for item in ls:
        print("{}".format(item))
    #print("\n")
        
def print_tuples_list(ls):
    for item in ls:
        index, ticker, date, time, price = item
        print("{0} {1} {2} {3}".format(ticker, date, time, price))
        