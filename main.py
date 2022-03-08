# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 12:32:04 2022

Contains all classes dealing with front-end program interaction

@author: Dylan Munro
"""

import src.assets.manager as manager
import tests.tests as tests

from typing import Final

import pandas as pd

"""
Handles all IO requests from the user

class variables:
    file - The file which stores asset data if not using coingecko API
"""
class IO:
    
    #Final means static class checkers wont reassign. Must import Final from typing
    _SUPPORTED_FILES:Final = {".csv", ".xlsx"}
    _DEFAULT_FILE:Final = "resources/spreadsheets/MaticVsLrcPrices.xlsx"
    
    def __init__(self):
        self._driver = None
        
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
                    self._driver = manager.Driver(df)
                    file_loaded = True
                except (ValueError, FileNotFoundError) as e:
                    print("{}".format(e))
                    response = self.get_yes_no_response("Would you like to try loading a different file? (Yes/No)\n")
                    if response == "no":
                        self.load_default_file()
                        file_loaded = True
        else: #Load the default file
            self.load_default_file()
    
    def load_default_file(self):
        print("Loading default file at {}".format(IO._DEFAULT_FILE))
        df = self.load_file(IO._DEFAULT_FILE)
        self._driver = manager.Driver(df)
    
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
        #self._driver = manager.Driver(self.load_file(IO._DEFAULT_FILE))
        self.run()
        
    def run(self):
        user_num = 0
        prompt = self.get_prompt()
        standalone_requests = manager.Request.get_STANDALONE_REQUESTS()
        while not user_num == manager.Request.QUIT:
            try:
                #Name of the asset that the request is acting on
                assets = None
                assets_list = None
                
                #Check if user enters a valid number
                response = input(prompt)
                if not response.isnumeric():
                    raise ValueError("Please enter an integer")
                user_num = int(response)
                if not manager.Request.is_valid_value(user_num):
                    raise ValueError("Please enter an integer between {} and {}"
                                         .format(manager.Request.get_smallest_value(), 
                                                 manager.Request.get_largest_value()))
                    
                #Obtain name of asset request is acting on if necessary
                if not user_num in standalone_requests:
                    assets = input("Enter the name of the asset(s) (case-sensitive), separating them by spaces:\n")
                    assets_list = assets.split(" ")
                request = manager.Request(user_num, assets=assets_list)
                print(self._driver.execute_request(request))
            except (ValueError, UserWarning) as e:
                print(e)
    
    def get_prompt(self):
        """
        Returns all valid requests and their descriptions
        """
        requests = manager.Request.get_VALID_REQUESTS()
        key_list = list(requests.keys())
        temp = [""]
        for i in key_list:
            temp.append("Press ")
            temp.append(str(i))
            temp.append(" to ")
            temp.append(requests[i])
            temp.append("\n")
        return "".join(temp)

if __name__ == "__main__":
    IO().main()
    #tests.graph_tests()
