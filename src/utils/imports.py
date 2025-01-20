# Imports from rich library
from rich.console import Console
from rich.progress import Progress
from rich.prompt import Prompt
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table
from rich.text import Text
from rich import box
from rich import print

# Classes
from services.login import Login
from services.clear import TerminalClear
from services.loader import Loader
from services.logs import Logger
from logic.dream_handler import DreamHandler
from logic.journal_handler import JournalHandler

# Packages
import sys
import os
import json
import time

# Functions

def clear():
  TerminalClear.clear()