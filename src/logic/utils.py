import os
import re
import sys
import termios
import tty
from datetime import datetime

# A dictionary to map month names to numbers for formatting purposes.
MONTHS_REVERSED = {
    "January": "01", "February": "02", "March": "03", "April": "04",
    "May": "05", "June": "06", "July": "07", "August": "08",
    "September": "09", "October": "10", "November": "11", "December": "12"
}

class Helpers:
    @staticmethod
    def extract_date_from_file(file_path):
        """
        Extract the dream date from a file.

        Arguments:
            file_path (str): The file's path to read.

        Returns:
            str: The extracted date or 'DirtyEntry' if the date is missing or an error occurs.
        """
        try:
            date_pattern = r"\[.*\| (.*) \]"

            with open(file_path, 'r') as file:
                content = file.read()
                match = re.search(date_pattern, content)
                if match:
                    return match.group(1)
                else:
                    print("Date pattern not found in file.")
                    return 'DirtyEntry'
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return 'DirtyEntry'

    @staticmethod
    def date_formatter(date_unformatted, flipped, bracket_bug=False):
        """
        Format a date string into the numerical version: [YYYY-MM-DD].

        Arguments:
            date_unformatted (str): The unformatted date.
            flipped (bool): True for [Month Day, Year], False for [Day Month, Year].
            bracket_bug (bool): True if the year has an extra closing bracket to remove.

        Returns:
            str: The formatted date or 'DirtyEntry' if the string is malformed.
        """
        try:
            parts = date_unformatted.split(',')
            if len(parts) == 2:
                day_month = parts[0].strip().removeprefix('(')
                year = parts[1].strip()[:-1] if bracket_bug else parts[1].strip()

                day_month_parts = day_month.split()
                if len(day_month_parts) == 2:
                    if flipped:
                        month, day = day_month_parts
                    else:
                        day, month = day_month_parts

                    if month in MONTHS_REVERSED:
                        if day.isdigit() and 1 <= int(day) <= 31:
                            return f"{year}-{MONTHS_REVERSED[month]}-{day.zfill(2)}"
        except Exception as e:
            print(f"Error formatting date {date_unformatted}: {e}")
        return 'DirtyEntry'

    @staticmethod
    def list_files(directory):
        """
        List all text files in a directory structure sorted by year, month, day, and creation time.

        Arguments:
            directory (str): The directory to scan.

        Returns:
            list: Sorted list of file paths.
        """
        files = []

        for root, _, file_names in os.walk(directory):
            for file_name in file_names:
                if file_name.endswith(".txt"):
                    file_path = os.path.join(root, file_name)

                    # Extract the date from the directory structure (year, month, day)
                    parts = os.path.normpath(root).split(os.sep)
                    try:
                        year = int(parts[-3])
                        month = datetime.strptime(parts[-2], "%B").month
                        day = int(parts[-1])
                        file_date = datetime(year, month, day)
                    except (IndexError, ValueError):
                        file_date = datetime.min

                    
                    # Get the creation time using os.path.getctime
                    creation_time = os.path.getctime(file_path)

                    # Append the file details to the list
                    files.append((file_date, creation_time, file_path))

        # Sort by file_date first, and if dates are the same, by creation time
        files.sort(key=lambda entry: (entry[0], entry[1]), reverse=True)  # Descending order

        return [file_path for _, _, file_path in files]

    @staticmethod
    def getch():
        """
        Get a single character from standard input.

        Returns:
            str: The pressed character.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch