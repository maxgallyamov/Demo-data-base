# script.py
# --------------------------------------------------------------------
# Project: Algorithm for Data Processing
# Author: Maksim Gallyamov
# Description: Processing and scanning for the presence of new data, as well as copying it
# Version: 0.3.1 07-30-2024 --

import os
import shutil
import sqlite3
from datetime import datetime
import json

CONFIG_FILE = ".\\config.json"

print(f'.\\config.json: {CONFIG_FILE}') 

# Loading the configuration file
def load_config(config_file):
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
    
    with open(config_file, 'r', -1, 'utf_8_sig') as file:
        return json.load(file)

# Saving the updated configuration file
def save_config(config_file, config):
    
    with open(config_file, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4)

# Converting strings with the last script run date to a datetime object
def get_last_run_time(last_run_time_str):
    try:
        
        return datetime.strptime(last_run_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        
        print(f"Error: Invalid date format in last_run_time: {last_run_time_str}.")
        exit(1)  # Завершаем выполнение скрипта с ошибкой

# Getting the last modification time of a file
def get_file_modification_time(file_path):
    try:
        
        mod_time = os.path.getmtime(file_path)
        return datetime.fromtimestamp(mod_time)
    except FileNotFoundError:
        
        print(f"Error: File {file_path} not found.")
        return None

# Reading the configuration file
def main():
    try:
    
       config = load_config(CONFIG_FILE)
       if 'source_directory' not in config:
           raise KeyError("Key 'source_directory' not found in configuration file.")
       if 'destination_directory' not in config:
           raise KeyError("Key 'destination_directory' not found in configuration file.")
    
       source_path = config['source_directory']
       destination_path = config['destination_directory']
       last_run_time_str = config['last_run_time']
       last_run_time = get_last_run_time(last_run_time_str)
    
       if not os.path.isdir(source_path):
          raise NotADirectoryError(f"Source directory '{source_path}' does not exist.")
    
       print(f"Source Path: {source_path}")
       print(f"Destination Path: {destination_path}")
       print(f"Last Run Time: {last_run_time}")
    
       # Extracting the list of files from the source directory
       files = os.listdir(source_path)
    
       print(f"Files in Source Directory ({source_path}):")
       for file in files:
           file_path = os.path.join(source_path, file)
           file_mod_time = get_file_modification_time(file_path)
        
           print(f"File: {file} - Last Modified: {file_mod_time}")
           if file_mod_time > last_run_time:
              print(f"    {file} has been modified since the last run.")
              destination_file_path = os.path.join(destination_path, file)  
              shutil.copy2(file_path, destination_file_path)
           else:
               print(f"    {file} has not been modified since the last run.")
          # Updating the last run time in the configuration file
           current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
           config['last_run_time'] = current_time
           save_config(CONFIG_FILE, config)    
    except FileNotFoundError as err:
     print(f"Error: {err}")
    except KeyError as err:
     print(f"Error: {err}")
    except NotADirectoryError as err:
     print(f"Error: {err}")
    except Exception as err:
     print(f"An unexpected error occurred: {err}")

# Starting the main process
if __name__ == "__main__":
    main()