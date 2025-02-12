# Main logic handler
# @RanbirSDeol
# 1/17/2025

__version__ = "1.0.0"

from utils.imports import *

# Constants
PROGRAM_TITLE = f"Journal Plus"  # Global program title
LOADING_SPEED = 0.005

# Function to load our settings json file
def load_settings(file_path):
    try:
        with open(file_path, 'r') as file:
            settings = json.load(file)
            return settings
    except FileNotFoundError:
        print(f"Error: Settings file '{file_path}' not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in '{file_path}'.")
        return {}

# Safely get nested values
def get_nested(data, keys, default=None):
    """
    Retrieve a nested value from a dictionary.
    """
    keys_list = keys.split('.')
    for key in keys_list:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return default
    return data

# Vars
settings_path = './settings.json'
settings = load_settings(settings_path)
console = Console()
logs = Logger(settings_path)

# Panels
def print_title():
    title = Panel(PROGRAM_TITLE, style="bold #F8B195", width=16)
    console.print(title)

def print_prompt():
    prompt_text = "[bold white]Enter a command[/bold white] (type [bold green]'help'[/bold green] for commands)"
    prompt = Panel(prompt_text, width=47)
    console.print(prompt)
    
def print_command(user_command):
    panel = Panel(f"[bold white]Command[/bold white]: {user_command}", expand=False)
    console.print(panel)

def print_unknown(input_command):
    unknown_command = Panel(f"[bold red]Unknown Command[/bold red]: {input_command}", expand=False)
    console.print(unknown_command)

def print_panel(content, color, style, width):
    panel = Panel(f"[{color}]{content}[/{color}]", style=f"bold {style}", width=width)
    console.print(panel)

# Function to login the user using their pin
def login():
    """Main login loop"""
    login_system = Login()  # Initialize the login system
    
    while True:
        logged_in = login_system.login()
        
        if not logged_in:    
            clear()
            # Prompt user to either try again or quit
            print_panel("Incorrect PIN!", "bold red", "red", 18)
            print_panel("Enter 'q' to quit or press 'enter' to try again: ", "white", "white", 38)
            user_input = Prompt.ask("", show_default=False)
            
            if user_input.lower() == 'q':
                console.print("[bold red]Exiting program...[/bold red]")
        else:
            # Create a Progress object
            clear()
            with Progress() as progress:
                task = progress.add_task("[white]Logging in...", total=100)
                
                # Simulate some work (this will update the progress bar)
                while not progress.finished:
                    progress.update(task, advance=1)
                    time.sleep(LOADING_SPEED)
            break 

# Function that ensures all files and directories exist
def loader():
    validator = Loader(settings_path)

    # Validate directories
    if not validator.validate():
        logs.log("ERROR", "One or more directories are missing")

# Function to display all commands
def display_help():
    '''
    A function that displays all commands
    '''

    table = Table()

    # Add columns
    table.add_column("Commands", justify="left", style="bold green")
    table.add_column("Description", justify="left")

    # Program commands
    table.add_row("[purple]'dream'[/purple]", "Open your dream journal")
    table.add_row("[yellow]'journal'[/yellow]", "Open your journal")
    
    table.add_row("", "")
    
    # Console commands
    table.add_row("[green]'logs'[/green]", "Display your logs")
    table.add_row("[red]'clr_logs'[/red]", "Clear your logs")
    
    table.add_row("", "")
    
    table.add_row("[green]'help'[/green]", "Display the help menu")
    table.add_row("[green]'clear'[/green]", "Clear your terminal")
    
    table.add_row("", "")
    
    table.add_row("[blue]'update'[/blue]", "Update the program")
    table.add_row("[green]'quit'[/green]", "Quit the program")

    # Print the table
    console.print(table)

# Function to clear the terminal
def clear_terminal():
    clear()
    print_title()
    panel = Panel(f"[bold green]Command[/bold green]: clear", expand=False)
    console.print(panel)

# Function to handle dream journal
def dream_journal():
    # Run the dream journal sub task
    dream_manager = DreamHandler()
    dream_manager.run()
    
    # Once completed show title again to alert user they're in the hub
    print_title()
    
# Function to handle journal
def journal():
    # Run the dream journal sub task
    journal_manager = JournalHandler()
    journal_manager.run()
    
    # Once completed show title again to alert user they're in the hub
    print_title()
   
# Function to update the program
def update():
    print("UPDATE", f"Attempting Update!")
    
    # Create a Progress bar instance
    with Progress() as progress:
        # Add the task with a description
        clear()
        task = progress.add_task("[white]Updating repository...", total=100)

        # List all the directories with .pyc files
        pycache_dirs = [
            "logic/__pycache__/",
            "services/__pycache__/",
            "logic/models/__pycache__/",
            "utils/__pycache__/"
        ]
        
        try:
            # Absolute path for repo root (adjust if necessary)
            repo_root = os.path.abspath(os.path.dirname(__file__))

            # Manually remove .pyc files from the directories
            for pycache_dir in pycache_dirs:
                full_path = os.path.join(repo_root, pycache_dir)
                
                # Ensure the directory exists
                if os.path.exists(full_path):
                    # Walk through the directory and remove .pyc files
                    for root, dirs, files in os.walk(full_path):
                        for file in files:
                            if file.endswith(".pyc"):
                                os.remove(os.path.join(root, file))  # Delete the .pyc file
                else:
                    print(f"[bold yellow]Warning: {full_path} does not exist.[/bold yellow]")

            # Change to the parent directory (where the .git repo is located)
            parent_directory = os.path.dirname(repo_root)
            os.chdir(parent_directory)  # Move to the parent directory

            # Check if there are local changes that need to be committed or stashed
            result = subprocess.run(["git", "diff", "--exit-code"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                print("[bold yellow]Warning: You have uncommitted changes. Stashing them for you...[/bold yellow]")
                subprocess.run(["git", "stash"], check=True)  # Stash the changes

            # Now fetch the latest updates
            subprocess.run(["git", "fetch"], check=True)

            # Simulate progress update
            while not progress.finished:
                progress.update(task, advance=10)
                time.sleep(0.1)

            # After fetch, perform a pull to update the working directory
            subprocess.run(["git", "pull"], check=True)

            # Complete the progress bar
            progress.update(task, completed=100)
            
            print("[bold green]Update Success! Please restart program[/bold green]")  # For success message
            sys.exit()  # Exit, and make the user reload
        except subprocess.CalledProcessError as e:
            print(f"[bold red]Error occurred while updating: {e}[/bold red]")
   
# Function to exit the program 
def quit_program():
    clear()
    sys.exit()
    
# Function to handle commands from user
def handle_commands(input_command):
    '''
    A function that connects all commands to their functions
    '''

    commands = {
        "dream": dream_journal,
        "d": dream_journal, # shortcut
        "journal": journal,
        "j": journal, # shortcut
        "logs": logs.display,
        "clr_logs": logs.clear,
        "help": display_help,
        "clear": clear_terminal,
        "quit": quit_program,
        "update": update,
        "q": quit_program # shortcut
    }

    command_func = commands.get(input_command)
    if command_func:
        command_func()
    else:
        print_unknown(input_command)

# Main loop
def main():
    """Main program loop"""
    clear()
    print_title()
    
    user_command = ""
    
    while True:
        # Create a border with your prompt text inside
        print_prompt()
        print_command(user_command)

        # Ask user for input
        user_command = Prompt.ask("", default="", show_default=False).lower()
        
        clear()
        print_title()
        handle_commands(user_command)

if __name__ == "__main__":
    # Login the user
    login()
    
    # Validate directories
    loader()
    
    # Start main loop
    main()