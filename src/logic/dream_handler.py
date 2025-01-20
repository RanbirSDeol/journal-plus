# Dream class
# This class will handle the dream journal
# @RanbirSDeol
# 1/17/2025

# Modules
import sys
import os
import re
import termios
import subprocess
import tty
import time
import random
import json
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from collections import Counter
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
from matplotlib.ticker import MaxNLocator

# Classes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.imports import *
from .models.dream import Dream
from .utils import Helpers

# Settings.json
script_dir = os.path.dirname(os.path.abspath(__file__))
settings_file_path = os.path.join(script_dir, '..', 'settings.json')

# Load the JSON file
with open(settings_file_path, 'r') as file:
    config = json.load(file)

# Load our settings.json
SMTP_SERVER = config['smtp']['server']
SMTP_PORT = config['smtp']['port']
JOURNAL_DIR = config['directories']['dreams']
SYNC_SPEED = 0.05 # Change to settings | Slow it is, the more reliable the sync is

# A list of all the months, to be used to convert number month to word month
MONTHS = [
    None, 'January', 'February', 'March', 'April', 'May', 
    'June', 'July', 'August', 'September', 'October', 'November', 'December'
]

# A list of all the months mapped to a number, used to convert word months to numbers
MONTHS_REVERSED = {
    "January": '01',
    "February": '02',
    "March": '03',
    "April": '04',
    "May": '05',
    "June": '06',
    "July": '07',
    "August": '08',
    "September": '09',
    "October": '10',
    "November": '11',
    "December": '12'
}

# Vars
console = Console()

# Global constants
PROGRAM_TITLE = "Dream Journal"

script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to sync-dream.txt in the grandparent directory
sync_file_path = os.path.join(script_dir, '..', '..', 'data', 'sync-dream.txt')
backup_file_path = os.path.join(script_dir, '..', '..', 'data', 'backups')

# Use the dynamically constructed path for the SYNC_FILE
SYNC_FILE = sync_file_path
BACKUP_DIRECTORY = backup_file_path

settings_path = os.path.join(script_dir, '..', 'settings.json')
# Pass the dynamically constructed path to the Logger
logs = Logger(settings_file=settings_path)


# Local Function
        
def clear():
    console.clear()

class DreamHandler:
    def __init__(self):
        self.journal_dir = JOURNAL_DIR
    
    # | Local Functions |
    def print_panel(self, content, color, style, width):
        panel = Panel(f"[{color}]{content}[/{color}]", style=f"bold {style}", width=width)
        console.print(panel)
    def print_title(self):
        title = Panel(f"[purple]{PROGRAM_TITLE}[/purple]", style="bold white", width=17)
        console.print(title)
    def print_prompt(self, command):
        if not command:
            prompt_text = "[bold white]Command: [/bold white]"
            prompt = Panel(prompt_text, width=14)
            console.print(prompt)
        else:
            prompt_text = f"[bold white]Command: {command} [/bold white]"
            prompt = Panel(prompt_text, width=14)
            console.print(prompt)
    def print_command(self, user_command):
        panel = Panel(f"[bold green]Command[/bold green]: {user_command}", expand=False)
        console.print(panel)
    def print_unknown(self, input_command):
        unknown_command = Panel(f"[bold red]Unknown Command[/bold red]: {input_command}", expand=False)
        console.print(unknown_command)
     
    # | Program | 
    def navigate(self):
        """
        Function to navigate through our dream journal
        
        Arguments:
            None

        Returns:
            None
        """
        
        # Our files
        dream_files = Helpers.list_files(self.journal_dir)[::-1]

        # Make sure we have dream files
        if not dream_files:
            self.print_panel("No Dream Entries Found!", "bold yellow", "yellow", 75)
            index = 0
        else:
            index = len(dream_files) - 1

        # Store our command previously entered
        command = ""

        while True:
            
            clear()
            
            # Make sure we have dream files
            if not dream_files:
                self.print_panel("No Dream Entries Found!", "bold yellow", "yellow", 75)
            
            # Wrap index around if it goes out of bounds
            index = index % len(dream_files) if dream_files else 0

            if dream_files:
                # Display the current dream entry in a panel
                dream_file = dream_files[index]

                try:
                    with open(dream_file, 'r') as file:
                        dream = Dream.from_file(file.read())
                        
                    # Index starts from 1
                    current_index = index + 1
                    total_entries = len(dream_files)
                    
                    # Display

                    index_panel = Panel(
                        Text(f"[{current_index} / {total_entries}]", justify="center"),
                        title="Index",
                        border_style="white",
                        box=box.ROUNDED,
                        width=17,
                    )

                    # Create a table for the title and date
                    title_table = Table(border_style="white", box=box.ROUNDED, width=75)

                    # Add columns to the table
                    title_table.add_column("Dream Title", justify="left", style="italic", width=20)
                    title_table.add_column("Dream Date", justify="left", style="italic", width=10)

                    # Add a row with the dream title and date
                    title_table.add_row(dream.title, dream.date)

                    # Create a table for the stats
                    stats_table = Table(border_style="white", box=box.SQUARE, width=75)
                    stats_table.add_column("Statistics", justify="left", style="bold green", width=8)
                    stats_table.add_column("Value", justify="left", style="white", width=25)

                    # Add rows for each stat
                    stats_table.add_row("Dream Type", dream.dream_type)
                    stats_table.add_row("Technique", dream.technique)
                    stats_table.add_row("Sleep Cycle", dream.sleep_cycle)

                    # Panel for the dream content
                    content_panel = Panel(
                        dream.entry,
                        title="Dream Content",
                        border_style="white",
                        box=box.ROUNDED,
                        width=75
                    )

                    # Print all content before commands
                    TerminalClear.clear()
                    self.print_title()
                    console.print(index_panel)
                    console.print(title_table)
                    console.print(stats_table)
                    console.print(content_panel)
                except Exception as e:
                    logs.log("ERROR", f"[bold red]Error reading file: {os.path.basename(dream_file)} - {str(e)}[/bold red]")

            # Create a horizontal table for the commands
            command_table = Table(
                show_header=False, box=box.SQUARE, border_style="white", width=75
            )
            command_table.add_column("Command", justify="center", style="bold green")
            command_table.add_row("(c)reate | (d)elete | (n)ext | (p)rev | (f)ind | (i)ndex | (a)nalytics | (b)ackup | (s)ync | (q)uit")
            console.print(command_table)
            self.print_prompt(command)

            # Ask user for input
            user_command = Helpers.getch().lower()
            command = user_command

            # Next File
            if user_command == "n" and dream_files:
                index -= 1
                self.print_prompt(user_command)
                
            # Previous File
            elif user_command == "p" and dream_files:
                index += 1
                self.print_prompt(user_command)
                
            # Create File
            elif user_command == "c":
                TerminalClear.clear()
                self.print_title()
                self.create_dream()
                dream_files = Helpers.list_files(self.journal_dir)[::-1]
                index = len(dream_files) - 1
            
            # Edit File
            elif user_command == "e" and dream_files:
                self.print_prompt(user_command)
                self.edit_dream(dream_files[index])
                dream_files = Helpers.list_files(self.journal_dir)[::-1]
                
            # Index File
            elif user_command == "i" and dream_files:
                # Getting our index location we want to navigate to
                self.print_panel("Enter Index:", "white", "white", 14)
                index_location = Prompt.ask("", show_default=False)
                
                try:
                    index_location = int(index_location)
                    if 0 <= index_location <= len(dream_files):
                        index = index_location - 1
                except Exception as e:
                    pass
                
            # Delete File
            elif user_command == "d" and dream_files:
                random_number = random.randint(1000, 9999)
        
                # Display the prompt with the random number
                self.print_panel(f"Enter Number To Delete Index [{index + 1}]: {random_number}", "bold red", "red", 75)
                user_input = Prompt.ask("", show_default=False)
                
                # Check if the entered number matches the generated number
                if user_input == str(random_number):
                    self.delete_dream(dream_files[index])
                    dream_files = Helpers.list_files(self.journal_dir)[::-1] # Re-fetch the dream files after deletion
                    index = index - 1
            
            # Sync Files
            elif user_command == "s":
                # Ask for confirmation before syncing
                self.print_panel("Do you want to sync your entries? (y/n):", "bold white", "white", 75)
                sync_confirm = Prompt.ask("", show_default=False)
                
                if sync_confirm == "y":
                    clear()
                    self.print_prompt(user_command)
                    self.sync()  # Proceed with syncing
                    dream_files = Helpers.list_files(self.journal_dir)[::-1]  # Re-fetch the dream files after syncing
                else:
                    console.print("[bold yellow]Sync canceled.[/bold yellow]")
                dream_files = Helpers.list_files(self.journal_dir)[::-1]   
                      
            # Find Files
            elif user_command == "f" and dream_files:
                # Prompt the user for a search keyword
                self.print_panel("Search Keyword:", "bold white", "white", 45)
                search_keyword = Prompt.ask("", show_default=False)
                
                # Gather a list of files that match the search phrase along with their original index
                matching_files = []
                for index, file in enumerate(Helpers.list_files(self.journal_dir)):
                    with open(file, 'r') as f:
                        content = f.read()
                        # Use a regex to match whole words only (case-insensitive)
                        if re.search(rf'\b{re.escape(search_keyword)}\b', content, flags=re.IGNORECASE):
                            matching_files.append((file, index))

                # Reverse the list of matching files
                matching_files = matching_files[::-1]
                
                # If no matches found, log an error
                if not matching_files:
                    self.print_panel(f"No Matches For: {search_keyword}", "bold red", "red", 75)
                    time.sleep(1)
                else:
                    search_index = len(matching_files) - 1

                    # New search-based navigation
                    while True:
                        # Clear the terminal
                        TerminalClear.clear()

                        # Get the current dream file based on the search index
                        search_dream_file, _ = matching_files[search_index]

                        try:
                            with open(search_dream_file, 'r') as file:
                                dream = Dream.from_file(file.read())

                            # Index starts from 1, not 0
                            current_index = search_index + 1
                            total_entries = len(matching_files)

                            index_panel = Panel(
                                Text(f"[{current_index} / {total_entries}]", justify="center"),
                                title="Index",
                                border_style="white",
                                box=box.ROUNDED,
                                width=17,
                            )

                            # Create a table for the title and date
                            title_table = Table(border_style="white", box=box.ROUNDED, width=75)

                            # Add columns to the table
                            title_table.add_column("Dream Title", justify="left", style="italic", width=20)
                            title_table.add_column("Dream Date", justify="left", style="italic", width=10)

                            # Create a Text object for the title
                            highlighted_title = Text(dream.title)

                            # Highlight all occurrences of the search_keyword (case-insensitive)
                            highlighted_title.highlight_regex(
                                rf"(?i){re.escape(search_keyword)}",  # (?i) makes it case-insensitive
                                style="bold yellow"
                            )

                            # Add a row with the dream title and date
                            title_table.add_row(highlighted_title, dream.date)

                            # Create a table for the stats
                            stats_table = Table(border_style="white", box=box.SQUARE, width=75)

                            # Add columns to the table
                            stats_table.add_column("Statistics", justify="left", style="bold green", width=8)
                            stats_table.add_column("Value", justify="left", style="white", width=25)

                            # Add rows for each stat
                            stats_table.add_row("Dream Type", dream.dream_type)
                            stats_table.add_row("Technique", dream.technique)
                            stats_table.add_row("Sleep Cycle", dream.sleep_cycle)

                            # Create a Text object for the content
                            highlighted_entry = Text(dream.entry)

                            # Highlight all occurrences of the search_keyword (case-insensitive)
                            highlighted_entry.highlight_regex(
                                rf"(?i){re.escape(search_keyword)}",  # (?i) makes it case-insensitive
                                style="bold yellow"
                            )

                            # Panel for the dream content
                            content_panel = Panel(
                                highlighted_entry,
                                title="Dream Content",
                                border_style="white",
                                box=box.ROUNDED,
                                width=75
                            )

                            # Print all content before commands
                            TerminalClear.clear()
                            self.print_title()
                            console.print(index_panel)
                            console.print(title_table)
                            console.print(stats_table)
                            console.print(content_panel)

                        except Exception as e:
                            logs.log("ERROR", f"[bold red]Error reading file: {os.path.basename(search_dream_file)} - {str(e)}[/bold red]")

                        # Create a horizontal table for the commands
                        command_table = Table(
                            show_header=False, box=box.SQUARE, border_style="white", width=75
                        )
                        command_table.add_column("Command", justify="center", style="bold green")

                        # Add the commands in a horizontal format
                        command_table.add_row("(n)ext | (p)revious | (q)uit")
                        console.print(command_table)

                        # Ask user for input
                        user_command = Helpers.getch().lower()

                        # Handle navigation commands
                        if user_command == 'n':
                            search_index = (search_index - 1) % len(matching_files)  # Move to the next result
                        elif user_command == 'p':
                            search_index = (search_index + 1) % len(matching_files)  # Move to the previous result
                        elif user_command == 'q':
                            break  # Exit the search navigation loop
            
            # Backup Files
            elif user_command == "b" and dream_files:
                # Ask for confirmation before syncing
                self.print_panel("Do you want to backup your entries? (y/n):", "bold white", "white", 75)
                backup_confirm = Prompt.ask("", show_default=False)
                
                if backup_confirm == "y":
                    self.backup() 
                else:
                    console.print("[bold yellow]Sync canceled.[/bold yellow]")
            
            # Show Dream Statistics
            elif user_command == "a" and dream_files:
                self.statistics()
            
            # Quit Dream Journal
            elif user_command == "q":
                TerminalClear.clear()
                break
        pass
    
    def edit_dream(self, path):
        """
        Edit the dream journal file using Emacs in the terminal.
        
        Arguments:
            path (str): The directory to scan for dream files.

        Returns:
            None
        """
        
        if os.path.exists(path):
            # Define the command to open the file in Emacs in the terminal
            TEXT_EDITOR = ["emacs", "-nw", path]
            
            try:
                # Use subprocess to open the file in Emacs
                subprocess.run(TEXT_EDITOR, check=True)
            except subprocess.CalledProcessError as e:
                logs.log("ERROR", f"[bold red]Failed to open {path} in Emacs.[/bold red]")
            except FileNotFoundError as e:
                logs.log("ERROR", "[bold red]Emacs is not installed or not found.[/bold red]")
        else:
            console.print(f"[bold red]The file {path} does not exist.[/bold red]")
    
    def create_dream(self):
        """
        Create a new dream entry and save it in the desired folder structure.
        
        Arguments:
            None

        Returns:
            None
        """

        # Prompt the user for the date in MM/DD/YYYY format using Rich
        while True:
            self.print_panel("Enter the date of the dream (MM/DD/YYYY) or ('q' to quit creation):", "bold white", "white", 75)
            date_input = Prompt.ask("", show_default=False)
            if date_input.lower() == 'q':
                return
            
            # Validate the date format
            try:
                date_obj = datetime.strptime(date_input, "%m/%d/%Y")
                month_name = date_obj.strftime("%B")  # Get full month name
                day = date_obj.day
                year = date_obj.year
                break  # Exit the loop if the date is valid
            except ValueError:
                self.print_panel(f"Invalid Date: ", "bold red", "red", 75)

        # Title panel
        clear()
        self.print_panel("Dream Title", "bold white", "white", 25)
        title_panel = Panel(
            Text("Enter a title for your dream entry:", justify="left"),
            style="bold white",
            width=40,
        )
        console.print(title_panel)
        title = Prompt.ask("", default="Untitled Dream", show_default=False)
        
        # Dream type panel
        clear()
        self.print_panel("Dream Type", "bold white", "white", 25)
        dream_type_panel = Panel(
            Text("Vague | Normal | Vivid | Vivimax | Lucid | Nightmare | No Recall:", justify="left"),
            style="bold white",
            width=75,
        )
        console.print(dream_type_panel)
        dream_type = Prompt.ask("", default="Lucid", show_default=False)
        
        # Dream technique panel
        clear()
        self.print_panel("Dream Technique", "bold white", "white", 25)
        technique_panel = Panel(
            Text("None | WILD | DILD | MILD | SSILD:", justify="left"),
            style="bold white",
            width=45,
        )
        console.print(technique_panel)
        technique = Prompt.ask("", default="WILD", show_default=False)

        # Sleep cycle panel
        clear()
        self.print_panel("Sleep Cycle", "bold white", "white", 25)
        sleep_cycle_panel = Panel(
            Text("Enter a sleep cycle (Regular | Nap | WBTB):", justify="left"),
            style="bold white",
            width=50,
        )
        console.print(sleep_cycle_panel)
        sleep_cycle = Prompt.ask("", default="REM", show_default=False)
        
        # Content panel
        clear()
        content_panel = Panel(
            Text("Would you like to open and edit the dream entry (y / n)?", justify="center"),
            style="bold white",
            width=75,
        )
        console.print(content_panel)
        
        edit_choice = Prompt.ask("", default="n", show_default=False)

        # Define the folder structure: year/month_name/day
        folder_path = os.path.join(self.journal_dir, str(year), month_name, str(day))

        # Create the directories if they don't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Generate timestamp for the file
        time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        
        # Create a file name based on the title and timestamp
        file_name = f"{title.replace(' ', '_')}_{time_stamp}.txt"
        
        # Make sure we the proper format
        entry_empty = "[ Dream Entry ]\n───────────────────────────────────────────────────────────────────────\n[]"
        
        # Create a new Dream object
        dream = Dream(
            title=title,
            dream_type=dream_type,  # Dynamic
            technique=technique,    # Dynamic
            sleep_cycle=sleep_cycle,  # Dynamic
            entry=entry_empty,  # Static
            date=f"{day} {month_name}, {year}",  # Format date as "Month Day, Year"
            date_created=datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Creation tag
        )

        # Write file
        new_path = os.path.join(folder_path, file_name)
        with open(new_path, 'w') as dream_file:
            dream_file.write(dream.format_dream_entry())
            
        # Open file if 'y'
        if edit_choice.lower() == 'y':
            self.edit_dream(new_path)
    
    def delete_dream(self, path):
        """
        Delete a dream entry by file path.
        
        Arguments:
            path (str): The directory to scan for dream files.

        Returns:
            None
        """
        if os.path.exists(path):
            os.remove(path)
            logs.log("INFO", f"[bold yellow]Deleted: {path}[/bold yellow]")

    def display_counter(self, counter, title):
        self.print_panel(f"{title}", "bold white", "white", 35)
        table = Table()
        table.add_column("Type", justify="left")
        table.add_column("Count", justify="right")

        # Sort the counter by count (value) in descending order
        sorted_items = sorted(counter.items(), key=lambda item: item[1], reverse=True)

        # Add rows to the table, excluding any items with a '+'
        for key, value in sorted_items:
            if '+' not in key:
                table.add_row(key, str(value))

        # Display the table
        console.print(table)

    def statistics(self):
        '''
        A function that goes through all the dream entries and returns the following statistics:
        - Dream Journals: X
        - All Categories:
            - Dream Types: {dream_types}
            - Techniques: {techniques}
            - Sleep Cycles: {sleep_cycles}
        - Streak: X
        '''
        exit_loop = False

        while not exit_loop:
            
            dream_type_count = Counter()
            technique_count = Counter()
            sleep_cycle_count = Counter()

            dream_dates = []  # List to store the dates of the dream entries
            dream_files = Helpers.list_files(self.journal_dir)

            if not dream_files:
                console.print(f"[yellow]No Dream Entries Found[/yellow]\n")
                return  # Early exit since there are no entries to process

            for file_path in dream_files:
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                    for i, line in enumerate(lines):
                        # Color the dream types
                        if i == 2 and "Lucid" in line:
                            line = line.replace("Lucid", f"[#FFD700]Lucid[/#FFD700]")
                        if i == 2 and "Vivid" in line:
                            line = line.replace("Vivid", f"[#00FF00]Vivid[/#00FF00]")
                        if i == 2 and "Nightmare" in line:
                            line = line.replace("Nightmare", f"[#FF5733]Nightmare[/#FF5733]")
                        if i == 2 and "Vague" in line:
                            line = line.replace("Vague", f"[#708090]Vague[/#708090]")
                        if i == 2 and "Vivimax" in line:
                            line = line.replace("Vivimax", f"[#FF69B4]Vivimax[/#FF69B4]")
                        if i == 2 and "No Recall" in line:
                            line = line.replace("No Recall", f"[#A9A9A9]No Recall[/#A9A9A9]")
                        if i == 2 and "Normal" in line:
                            line = line.replace("Normal", f"[#FFFFFF]Normal[/#FFFFFF]")
                        if i == 2 and "N/A" in line:
                            line = line.replace("N/A", f"[#ff0000]N/A[/#ff0000]")
                        if i == 2 and "IE" in line:
                            line = line.replace("IE", f"[#FF8C00]IE[/#FF8C00]")

                        # Color the dream techniques
                        if i == 3 and "WILD" in line:
                            line = line.replace("WILD", f"[#1E90FF]WILD[/#1E90FF]")
                        if i == 3 and "MILD" in line:
                            line = line.replace("MILD", f"[#ff0000]MILD[/#ff0000]")
                        if i == 3 and "SSILD" in line:
                            line = line.replace("SSILD", f"[#FF7F50]SSILD[/#FF7F50]")
                        if i == 3 and "DILD" in line:
                            line = line.replace("DILD", f"[#32CD32]DILD[/#32CD32]")

                        # Color the sleep cycles
                        if i == 4 and "Regular" in line:
                            line = line.replace("Regular", f"[gray]Regular[/gray]")
                        if i == 4 and "WBTB" in line:
                            line = line.replace("WBTB", f"[#00BFFF]WBTB[/#00BFFF]")
                        if i == 4 and "Nap" in line:
                            line = line.replace("Nap", f"[#9370DB]Nap[/#9370DB]")

                        # Update counters
                        if i == 2:
                            dream_types = line.split("Dream Type:")[1].strip().split(", ")
                            dream_type_count.update(dream_types)
                        elif i == 3:
                            techniques = line.split("Technique:")[1].strip().split(", ")
                            technique_count.update(techniques)
                        elif i == 4:
                            sleep_cycles = line.split("Sleep Cycle:")[1].strip().split(", ")
                            sleep_cycle_count.update(sleep_cycles)

                        # Store the date of the dream entry (assuming the date is on line 1)
                        if i == 0:
                            # Extract the date using Helpers.extract_date_from_file
                            date_str = line.split("|")[1].strip().replace("(", "").replace(")", "").replace(" ]", "")
                            logs.log("DEBUG", date_str)
                            try:
                                # Parse the date format (e.g., 19 January, 2025)
                                dream_dates.append(datetime.strptime(date_str, '%d %B, %Y'))
                            except ValueError:
                                pass  # If the date format is not valid, skip this entry

            max_streak = 0
            
            # Calculate the streak
            if dream_dates:
                logs.log("DEBUG", f"DREAM DATES FOUND {dream_dates}")
                dream_dates.sort()
                streak = 1
                max_streak = 1

                for i in range(1, len(dream_dates)):
                    # Check if the date is the previous day (streak continuation)
                    if (dream_dates[i] - dream_dates[i-1]).days == 1:
                        streak += 1
                    else:
                        streak = 1
                    max_streak = max(max_streak, streak)

            # Prepare statistics output
            num_dream_journals = len(dream_files)

            clear()
            self.print_panel(f"Analytics", "bold green", "green", 13)
            self.print_panel(f"[bold #FFD700]Streak[/bold #FFD700]: {max_streak}", "bold white", "white", 15)
            self.display_counter(dream_type_count, "Dream Type Counts")
            self.display_counter(technique_count, "Technique Counts")
            self.display_counter(sleep_cycle_count, "Sleep Cycle Counts")
            
            command_table = Table(
                show_header=False, box=box.SQUARE, border_style="white", width=10
            )
            command_table.add_column("Command", justify="center", style="bold green")
            command_table.add_row("(q)uit")
            console.print(command_table)
            user_command = Helpers.getch().lower()

            if user_command == "q":
                break
    
    def sync(self):
        """
        Sync loads a .txt file and reads all the contents. It then
        turns the text inside the body into a dream journal.
        """

        # A count to store how many files we've created
        files_created_count = 0

        try:
            # Open our sync.txt and read its contents
            with open(SYNC_FILE, 'r') as file:
                content = file.readlines()

            # Variable to store all entries in an organized manner
            organized_entries = []

            # Temporary variable to store the local entry
            entry = None
            capture_body = False

            for line in content:
                # Remove leading and trailing spaces
                line = line.strip()

                # Check if the line starts with our delimiter
                if line == "==============================":
                    # Check if an entry exists and append it to organized_entries
                    if entry and entry["Body"]:
                        organized_entries.append(entry)
                    # Initialize a new entry
                    entry = {"Date": "", "Title": "", "Body": "", "Dream Type": "", "Technique": "", "Sleep Cycle": ""}
                    capture_body = False

                # If we have an entry
                elif entry is not None:
                    if line.startswith("[ (") and "|" in line:
                        # Extract title and date
                        parts = line.split("|")
                        entry["Title"] = parts[0].strip("[ (")[:-1].strip()
                        entry["Date"] = parts[1].strip(") ]")[1:].strip()
                    elif line.startswith("Dream Type:"):
                        entry["Dream Type"] = line.split(":")[1].strip()
                    elif line.startswith("Technique:"):
                        entry["Technique"] = line.split(":")[1].strip()
                    elif line.startswith("Sleep Cycle:"):
                        entry["Sleep Cycle"] = line.split(":")[1].strip()
                    elif line.startswith("───────────────────────────────────────────────────────────────────────"):
                        # Don't capture the separator line itself, but keep the capture process going
                        continue
                    elif capture_body:
                        if entry["Body"]:
                            entry["Body"] += "\n"
                        entry["Body"] += line

                    # Start capturing body after separator
                    elif line.strip() and capture_body is False:
                        capture_body = True
                        entry["Body"] = line  # Start adding the body with the first non-separator line

            # If we have a valid entry at the end of the file, append it to organized_entries
            if entry and entry["Body"]:
                organized_entries.append(entry)

            # Set up the loading bar using Rich
            with Progress() as progress:
                task = progress.add_task("[cyan]Syncing dreams...", total=len(organized_entries))

                # Loop through the entries, and create a journal .txt for each
                for entry in organized_entries:
                    time.sleep(SYNC_SPEED) 
                    try:
                        entry["Body"] = entry["Body"].replace(
                            "[ Dream Entry ]",
                            "[ Dream Entry ]\n───────────────────────────────────────────────────────────────────────"
                        )
                        
                        # We'll split our date, to check if it is valid
                        day, month, year = Helpers.date_formatter(entry['Date'], False, False).split('-')
                        
                        date_str = f"{day}-{month}-{year}"  # "17-01-2024"
                        
                        date_obj = datetime.strptime(date_str, "%d-%m-%Y")
                        
                        month_name = date_obj.strftime("%B")
                        
                        # Generate timestamp for the file
                        time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                        
                        # Create a file name based on the title and timestamp
                        file_name = f"{(entry['Title']).replace(' ', '_')}_{time_stamp}.txt"
                        
                        # Create a new Dream object
                        dream = Dream(
                            title=(entry["Title"]),
                            dream_type=(entry["Dream Type"]),
                            technique=(entry["Technique"]), 
                            sleep_cycle=(entry["Sleep Cycle"]),
                            entry=(entry["Body"]),  # Static for now, can be updated
                            date=f"{day} {month_name}, {year}",  # Format date as "Month Day, Year"
                            date_created=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        )

                        # Define the folder structure: year/month_name/day
                        folder_path = os.path.join(self.journal_dir, str(year), month_name, str(day))
                        
                        # Create the directories if they don't exist
                        if not os.path.exists(folder_path):
                            os.makedirs(folder_path)

                        # For every file in the folder, remove their timestamp part and check
                        existing_files = os.listdir(folder_path)

                        # This handles the dream sync sort logic somehow :p
                        existing_file_base_names = [
                            file[:-27] if len(file) > 27 and file.endswith('.txt') else file
                            for file in existing_files
                        ]

                        # Check if the file name without the timestamp already exists
                        file_name_without_timestamp = (entry['Title']).replace(' ', '_')


                        if file_name_without_timestamp in existing_file_base_names:
                            continue
                        
                        # Write the formatted dream entry to the file
                        with open(os.path.join(folder_path, file_name), 'w') as dream_file:
                            dream_file.write(dream.format_dream_entry())
                        
                        files_created_count += 1

                    except Exception as e:
                        logs.log("ERROR", f"Failed to sync dreams: {e}")
                    
                    # Update the progress bar
                    progress.update(task, advance=1)

        except Exception as e:
            logs.log("ERROR", f"[bold red]Failed to sync dreams[/bold red]: {e}")

        # Log the total files created
        logs.log("SUCCESS", f"[bold green]Sync.txt Was Loaded! Files Created [/bold green]: {files_created_count}")
    
    def send_email(self, file_path):
        '''
        Sends the specified file via email.
        '''

        # Getting the email for the sender
        SENDER_EMAIL = input("Enter the email of the sender: ")
        # Getting the email for the reciever
        RECIPIENT_EMAIL = input("Enter the email of the reciever: ")

        # Google generated password, getting the sender_email is just extra security
        # This is a throwaway email
        SENDER_PASSWORD = 'zkgz avdi irab hwjg'

        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = 'Dream Vault Backup'

        body = 'Please find the attached backup of your dream journal.'
        msg.attach(MIMEText(body, 'plain'))

        attachment = open(file_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
        msg.attach(part)
        attachment.close()

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
            server.quit()
        except Exception as e:
            logs.log("ERROR", f"[red]Failed to send email[/red]: {e}")

    def backup(self):
        '''
        Backs up the dream journal files and sends the backup via email.
        '''

        # Let us get all the dream files
        dream_files = Helpers.list_files(self.journal_dir)

        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        backup_file_name = f"[{timestamp}]_Dream_Backup.txt"
        output_file_path = os.path.join(BACKUP_DIRECTORY, backup_file_name)

        with open(output_file_path, 'w') as output_file:  # Use 'w' to overwrite the file initially
            output_file.write("==============================\n")

        # Checking if we have any dreams
        if not dream_files:
            logs.log(f"\n[bold yellow]No Dream Entries Found To Backup[/bold yellow]\n")
        else:
            for file_path in dream_files:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    for i, line in enumerate(lines):
                        if line.startswith("[ ("):
                            match = re.search(r'\[ \((.*?)\) \| \((.*?)\) \]', line)
                            if match:
                                title = match.group(1)
                                date_str = match.group(2)
                                formatted_output = f"[ ({title}) | ({date_str}) ]\n"

                                # Join all lines except the last one in rest_of_content
                                rest_of_content = ''.join(lines[i + 1:])

                                full_output = formatted_output + rest_of_content
                                
                                full_output = re.sub(r"──────────────────────────────────────────────────────────────────────{35}", 
                                "───────────────────────────────────────────────────────────────────────", full_output)

                                with open(output_file_path, 'a') as output_file:
                                    output_file.write(full_output)
                                    output_file.write("\n\n==============================\n")

        self.send_email(output_file_path)
        logs.log("STATUS", f"[bold green]Backup Success [/bold green]: {backup_file_name}")
    
    def run(self):
        """Main loop for the Dream journal."""
        self.navigate() 