import logging
from colorama import Fore, Style
from constants.sizes import Logger_Level_Name_Size

"""
If we inheritence the `Formatter` in the python library of `logging`, 
we need to also done the function overloading of `format(self, record)`.

These formatters can be called to format the color or some other styles of the loggers.
"""

class BasicColorFormatter(logging.Formatter):
    """A Basic Color Formatter for Loggers"""
    def format(self, record):
        level_color = {
            logging.DEBUG: Fore.BLUE, 
            logging.INFO: Fore.GREEN, 
            logging.WARNING: Fore.YELLOW, 
            logging.ERROR: Fore.RED, 
            logging.CRITICAL: Fore.RED + Style.BRIGHT, 
        }
        color = level_color.get(record.levelno, Fore.WHITE)
        record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
        record.levelname = f"{record.levelname:^{Logger_Level_Name_Size}}" # centralize the level name
        return super().format(record)
    
class NullColorFormattter(logging.Formatter):
    "A Color Formatter for Loggers with Only Black or White Color"
    def format(self, record):
        level_color = {
            logging.DEBUG: Fore.WHITE, 
            logging.INFO: Fore.WHITE, 
            logging.WARNING: Fore.WHITE + Style.BRIGHT, 
            logging.ERROR: Fore.LIGHTBLACK_EX, 
            logging.CRITICAL: Fore.LIGHTBLACK_EX + Style.BRIGHT, 
        }
        color = level_color.get(record.levelno, Fore.WHITE)
        record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
        record.levelname = f"{record.levelname:^{Logger_Level_Name_Size}}" # centralize the level name
        return super().format(record)