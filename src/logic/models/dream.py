# dream.py

from datetime import datetime
import textwrap
import os
import re

class Dream:
    def __init__(self, title, dream_type, technique, sleep_cycle, entry, date=None, date_created=None, tags=None):
        self.title = title
        self.dream_type = dream_type
        self.technique = technique
        self.sleep_cycle = sleep_cycle
        self.entry = entry
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tags = self.extract_tags(entry)

    def extract_tags(self, entry):
        """Extract tags from the dream entry."""
        # Use a regular expression to find all occurrences of tags like -[TAG]-
        tags = re.findall(r'-\[(.*?)\]-', entry)
        return tags
    
    def load_dream_from_file(dream_file_path):
        """Load a dream from a saved file and return the Dream object."""
        try:
            with open(dream_file_path, 'r') as f:
                content = f.read()
            
            # Use the from_file method to create a Dream instance
            dream = Dream.from_file(content)
            
            print(f"Loaded dream: {dream.title}")
            return dream
        except Exception as e:
            print(f"Error loading dream from file: {e}")
            return None

    def format_dream_entry(self):
        """Format the dream into the template format."""
        dream_entry = f"""
[ ({self.title}) | ({self.date}) ]
──────────────────────────────────────────────────────────────────────
Dream Type: {self.dream_type}
Technique: {self.technique}
Sleep Cycle: {self.sleep_cycle}
──────────────────────────────────────────────────────────────────────
{self.entry}
        """
        # Remove the leading whitespace using textwrap.dedent
        return textwrap.dedent(dream_entry).strip()


    def save_to_file(self, journal_dir):
        """Save the formatted dream entry to a text file."""
        filename = f"{self.date}_{self.title.replace(' ', '_')}.txt"
        filepath = os.path.join(journal_dir, filename)
        with open(filepath, 'w') as f:
            f.write(self.format_dream_entry())
        print(f"Dream saved: {filename}")
        
    @classmethod
    def from_file(cls, content):
        """Load a dream from a file."""
        try:
            lines = content.split("\n")
            title_date = lines[0].strip(" []").split(" | ")
            title = title_date[0].strip("()")
            date = title_date[1].strip("()")
            metadata = lines[2:5]  # Dream Type, Technique, Sleep Cycle
            dream_type = metadata[0].split(":")[1].strip()
            technique = metadata[1].split(":")[1].strip()
            sleep_cycle = metadata[2].split(":")[1].strip()
            entry = "\n".join(lines[6:])
            entry = entry.replace("[ Dream Entry ]", "").strip()
            entry = entry.replace("───────────────────────────────────────────────────────────────────────", "").strip()
            tags = cls.extract_tags(cls, entry)
            return cls(title, dream_type, technique, sleep_cycle, entry, date=date, tags=tags)
        except Exception as e:
            raise ValueError(f"???")
