import os, sys, logging
from pathlib import Path
from datetime import datetime
from colorama import Fore, Style, init


init(autoreset=True)

def create_dirs(dir_path) -> Path:
    dir_path = Path(dir_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    
    return dir_path

# Logs directory
BASE_DIR = Path(__file__).parent.parent.parent
log_dir = BASE_DIR / "logs"

# Current date and create directory
current_date = datetime.now().strftime("%d-%m-%Y")
date_dir = os.path.join(log_dir, current_date)
create_dirs(date_dir)

# Current day and create directory
current_day = datetime.now().strftime("%A")
day_dir = os.path.join(date_dir, current_day)
create_dirs(day_dir)

def timestamp_dirs(base_time):
    try:
        timestamp = base_time.strftime("%d-%m-%Y_%H-%M")
        timestamp_dir = os.path.join(day_dir, timestamp)
        create_dirs(timestamp_dir)
        return timestamp_dir
    except Exception as e:
        raise Exception("Ërror in timestamp_dirs function: {e}")

# Current timestamp and create directory
base_time = datetime.now()
timestamp_dir = timestamp_dirs(base_time)

if timestamp_dir is None:
    raise Exception("Failed to create the timestamp directory for logging")

log_file_paths = {
    logging.INFO: os.path.join(timestamp_dir, 'info.log'),
    logging.DEBUG: os.path.join(timestamp_dir, 'debug.log'),
    logging.WARNING: os.path.join(timestamp_dir, 'warning.log'),
    logging.CRITICAL: os.path.join(timestamp_dir, 'critical.log'),
    logging.ERROR: os.path.join(timestamp_dir, 'error.log')
}

logs_format = "[ [%(asctime)s] : %(levelname)s : %(name)s : %(pathname)s : %(module)s : %(lineno)d : %(message)s ]"

logger = logging.getLogger("CodeChallengeGenerator")
logger.level
logger.propagate = False

# LevelFilter to allow only specific log levels
class LevelFilter(logging.Filter):

    def __init__(self, level):
        self._level = level
    
    def filter(self, record):
        return record.levelno == self._level

# File handler for each log level
def create_filehandler(level, log_file_path):
    try:
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(level)
        file_handler.addFilter(LevelFilter(level))
        file_handler.setFormatter(logging.Formatter(logs_format))
        return file_handler
    except Exception as e:
        raise Exception(f"Error in create_filehandler function: {e}")

# Avoid adding duplicate handlers
def add_handler_once(logger, handler):
    try:
        for h in logger.handlers:
            if (
                type(h) == type(handler)
                and
                getattr(h, 'baseFilenmae', None) == getattr(handler, 'baseFilenmae', None)
            ):
                return 
        logger.addHandler(handler)
    except Exception as e:
        raise Exception(f"Error in add_handler_once function: {e}")

# Add file handlers to the logger
for level, log_file_path in log_file_paths.items():
    handler = create_filehandler(level, log_file_path)
    
    if isinstance(handler, logging.FileHandler):
        add_handler_once(logger, handler)
    elif isinstance(handler, str):
        print(handler)

# Colors for log levels
def get_color_level(level):
    try:
        if level == logging.DEBUG:
            return Fore.LIGHTBLUE_EX
        elif level == logging.INFO:
            return Fore.LIGHTGREEN_EX
        elif level == logging.WARNING:
            return Fore.LIGHTYELLOW_EX
        elif level == logging.CRITICAL:
            return Fore.LIGHTMAGENTA_EX
        elif level == logging.ERROR:
            return Fore.LIGHTRED_EX
        else:
            return Fore.LIGHTWHITE_EX
    except Exception as e:
        raise Exception(f"Error in get_color_level function: {e}")


# Console handler for colored output
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# Custom Formatter for color-coding the console output
class ColorFormatter(logging.Formatter):

    def format(self, record):
        try:
            log_msg = super().format(record)
            color = get_color_level(record.levelno) or ""
            log_msg = log_msg or ""
            return color + log_msg + Style.RESET_ALL
        except Exception as e:
            print(f"Error in ColorFormatter class: {e}")
            return super().format(record)
    

# Setup console handler with color formatter
console_handler.setFormatter(ColorFormatter(logs_format))
add_handler_once(logger, console_handler)
