# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 10:02:19 2022

@author: dylmu
"""

import src.assets.manager as manager
import src.graphs.graph as graph

import pandas as pd

def data_manager_tests():
    """
    Function used to test the DataManager class
    """        
    df = pd.read_excel("resources/spreadsheets/functional.xlsx")
    try:
        dm = manager.DataManager(df)
        #entries = dm.get_entries("BTC")
        #print("Bitcoin entries: \n{}".format(dm.load_asset("BTC")))
        #dm.get_entries("ETH")
        #print("Ethereum Entries: \n{}".format(dm.load_asset("ETH")))
        #dm.load_entries("ETH")
        #dm.load_entries("BTC")
        dm.load_all()
        print(dm.get_visible_data())
        #dm.hide_all()
        #print(dm.get_visible_data())
        dm.hide_entry("BTC", "ETH")
        #dm.delete_asset("BTC")
        print("Entries:\n")
        #print(dm.get_visible_data())
        dm.load_entries("BTC", "ETH")
        print("Entries:\n")
        print(dm.get_visible_data())
        print("Loaded assets: \n")
        print_list(dm.get_visible_assets())
        print("\n")
        entries = dm.get_all_entries("BTC")
        print("Entries main: {}".format(entries))
        print_tuples_list(entries)
        #print("Visible entries for BTC:\n{}".format(self.print_list(dm.get_all_entries("BTC"))))
    except ValueError as e:
        print(e)
        
def graph_tests():
    """
    Function used to test graph functionality
    """
    df = pd.read_excel("resources/spreadsheets/functional.xlsx")
    try:
        dm = manager.DataManager(df)
        dm.load_all()
        my_graph = graph.Graph(dm.get_visible_data())
        my_graph.plot("BTC")
        my_graph.plot("ETH")
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
        