# Configuration variables and constants
import os

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
LOCAL_DIRECTORY = os.path.dirname(SCRIPT_DIRECTORY)

JOURNAL_DIRECTORY = os.path.join(LOCAL_DIRECTORY, 'journal')
BACKUP_DIRECTORY = os.path.join(LOCAL_DIRECTORY, 'backups')
LOGS_FILE = os.path.join(LOCAL_DIRECTORY, 'logs.txt')

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587