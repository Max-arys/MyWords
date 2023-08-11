from pathlib import Path

WORK_DIR = Path(__file__).resolve().parent
BASE_DIR = WORK_DIR.parent.parent
LOG_FILE = WORK_DIR.joinpath('data', 'logs.txt')
USERS_FILE = WORK_DIR.joinpath('data', 'users.json')
