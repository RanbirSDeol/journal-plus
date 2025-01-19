# Logs class
# This class will log information into logs.txt for the user
# @RanbirSDeol
# 1/17/2025

# Modules
import sys
import os
import logging
import json
from datetime import datetime

# Classes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.imports import *

class Logger:
    def __init__(self, settings_file="../settings.json"):
        """
        Initializes the Logger object to store logs in a text file based on the path specified in the settings file.
        """
        self.settings_file = settings_file
        self.log_file = self._load_log_file_path()

        # Set up logging configuration
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filemode='a'
        )

    def _load_log_file_path(self):
        """
        Loads the log file path from the settings.json file.
        """
        
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                # Extract the 'logs' path from the settings' paths section
                logs_path = settings.get('paths', {}).get('logs', '../data/logs.txt')  # Default if not found
                return logs_path
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Settings file {self.settings_file} not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON from {self.settings_file}.")

    def log(self, error_type, error_message):
        """
        Logs an error message in the format: ERROR_TYPE - ERROR_MESSAGE.
        """
        log_entry = f"{error_type} - {error_message}"
        logging.info(log_entry)
    
    def display(self):
        """
        Displays all the logs in the log file in a column format using rich.
        """
        try:
            with open(self.log_file, 'r') as file:
                console = Console()
                logs = file.readlines()
                table = Table()
                
                table.add_column("Timestamp", justify="center", style="cyan", no_wrap=True)
                table.add_column("Level", justify="center", style="magenta")
                table.add_column("Message", justify="left")

                # Parse and display each log entry in the table
                for log in logs:
                    # Assuming log format is: timestamp - level - message
                    parts = log.strip().split(" - ", 2)
                    if len(parts) == 3:
                        timestamp, level, message = parts
                        table.add_row(timestamp, level, message)

                # Print the table
                console.print(table)

        except FileNotFoundError:
            print(f"Log file {self.log_file} not found.")
        except Exception as e:
            print(f"Error displaying logs: {e}")

    def clear(self):
        """
        Clears the contents of the log file.
        """
        try:
            with open(self.log_file, 'w') as file:
                file.truncate(0)  # Clear the file content
            console = Console()
            console.print(Panel(f"Log file [magenta]{self.log_file}[/magenta] has been cleared.", style="bold white", width=35))
        except FileNotFoundError:
            print(f"Log file {self.log_file} not found.")
        except Exception as e:
            print(f"Error clearing logs: {e}")

# Example Usage:
if __name__ == "__main__":
    logs = Logger(settings_file="../settings.json")
    
    # Log different types of messages
    logs.log("ERROR", "This is an error message.")
    logs.log("INFO", "This is an informational message.")
    logs.log("WARNING", "This is a warning message.")
