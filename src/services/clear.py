# Clear class
# This class handles the clearing of the terminal
# @RanbirSDeol
# 1/17/2025

import os

class TerminalClear:
    @staticmethod
    def clear():
        """Clears the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
