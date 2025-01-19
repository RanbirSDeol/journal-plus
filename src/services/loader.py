# Loader class
# Ensures all directories exist and are valid
# @RanbirSDeol
# 1/17/2025

# Modules
import sys
import os
import json

# Classes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.imports import *

class Loader:
    def __init__(self, settings_file):
        '''
        Initialize with the path to the settings JSON file.
        '''
        self.settings_file = settings_file
        self.directories = self._load_directories()

    def _load_directories(self):
        '''
        Loads directories from the settings JSON file.
        '''
        with open(self.settings_file, 'r') as file:
            settings = json.load(file)
            # Extract the directories from the settings
            return list(settings.get("directories", {}).values())

    def validate(self):
        '''
        Checks if all directories in the settings file exist.
        '''
        for directory in self.directories:
            if not os.path.isdir(directory):
                return False
        return True