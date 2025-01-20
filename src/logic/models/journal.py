from datetime import datetime
import textwrap
import json

class Journal:
    def __init__(self, title, entry, date=None):
        self.title = title
        self.entry = entry
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        
    def format_journal_entry(self):
        """Format the journal into the template format."""
        dream_entry = f"""
[ ({self.title}) | ({self.date}) ]
───────────────────────────────────────────────────────────────────────
{self.entry}
        """
        # Remove the leading whitespace using textwrap.dedent
        return textwrap.dedent(dream_entry).strip()

    def save_to_file(self, file_path: str):
        """
        Save the journal entry to a file in JSON format.
        """
        data = {
            "title": self.title,
            "entry": self.entry,
            "date_created": self.date_created.strftime('%Y-%m-%d %H:%M:%S'),
            "date": self.date.strftime('%Y-%m-%d')
        }
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    @classmethod
    def from_file(cls, file_path: str):
        """
        Load a journal entry from a file.
        """
        with open(file_path, 'r') as file:
            data = json.load(file)
            date_created = datetime.strptime(data["date_created"], '%Y-%m-%d %H:%M:%S')
            journal = cls(data["title"], data["entry"])
            journal.date_created = date_created
            journal.date = date_created.date()
            return journal
       
    @classmethod 
    def from_file(cls, content):
        """Load a dream from a file."""
        try:
            # Split content by lines
            lines = content.split("\n")
            
            # Extract the title and date from the first line
            title_date = lines[0].strip(" []").split(" | ")
            title = title_date[0].strip("()")
            date = title_date[1].strip("()")
            
            # Find the start of the entry after the journal entry section
            entry_start_index = lines.index("[ Journal Entry ]") + 1
            entry = "\n".join(lines[entry_start_index:]).strip()
            
            # Remove any extra separator lines and clean up the entry text
            entry = entry.replace("───────────────────────────────────────────────────────────────────────", "").strip()
            
            return cls(title, entry, date=date)
        except Exception as e:
            raise ValueError(f"Error reading file: {e}")
