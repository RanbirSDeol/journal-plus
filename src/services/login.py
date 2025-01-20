# Login class
# This class will handle logging in of the user via a pin
# @RanbirSDeol
# 1/17/2025

# Modules
import sys
import os
import json

# Classes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.imports import *

console = Console()

class Login:
    def __init__(self):
        self.console = Console()
        self.settings_file = os.path.join(os.path.dirname(__file__), "../settings.json")  # Corrected path to settings.json
    
    def print_panel(self, content, color, style, width):
        panel = Panel(f"[{color}]{content}[/{color}]", style=f"bold {style}", width=width)
        console.print(panel)
    
    def load_settings(self):
        """Loads settings from the settings file."""
        # Make sure the path exists
        if not os.path.exists(self.settings_file):
            return {}
        
        with open(self.settings_file, "r") as f:
            return json.load(f)

    def verify_pin(self):
        """Verifies the entered PIN."""
        settings = self.load_settings()
        if "pin" not in settings:
            return False
        
        stored_pin = settings["pin"]

        console.clear()
        self.print_panel("Enter your PIN", "bold white", "white", 18)
        entered_pin = Prompt.ask("", show_default=False, password=True)
        
        if entered_pin == stored_pin:
            return True
        else:
            return False
    
    def login(self):
        """Main login process"""
        # Check for the PIN before proceeding
        if not self.verify_pin():
            return False
        else:
            # If the pin is correct or missing
            self.console.print("[bold cyan]Please enter your PIN.[/bold cyan]" if not self.load_settings().get("pin") else "")
            return True