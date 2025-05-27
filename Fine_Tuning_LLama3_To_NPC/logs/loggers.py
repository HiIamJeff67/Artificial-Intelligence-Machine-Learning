import os
import sys
import logging
from tqdm import tqdm
from typing import *
from pathlib import Path
from datetime import datetime
from logs.formatters import BasicColorFormatter
from colorama import Fore, Style
from constants.sizes import Logger_Level_Name_Size

class Logger:
    """A logger to log the test result, test procedures, exceptions, etc..."""
    
    def __init__(
        self, 
        title: str = "Undefined Title",
        output_file_name: str = None, 
        output_dir: str = None, 
        console_level: int = logging.INFO, 
        file_level: int = logging.DEBUG, 
        formatter: Type[logging.Formatter] = None,
        number_of_progress_bars: int = 1, 
    ):
        """
        Logger Initialization
        
        Args:
            title: a title of the currently running procedures
            output_file_name: a name for the output file
            output_dir: a path for the output file
            console_level: a logging level of the console
            file_level: a logging level of the file
            formatter: a custom type of formatter to format the logger
            number_of_progress_bars: the maximum number of progress bars which will be executed in the same time(not yet)
        """
        self.title = title
        self.output_file_name = output_file_name
        self.output_dir = output_dir
        
        if self.output_file_name is None:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_file_name = f"{'_'.join(self.title.lower().split(' '))}_output_{current_time}"
        
        if self.output_dir is None:
            self.output_dir = Path(os.path.dirname(os.path.abspath(__file__))) / "outputs"
        else:
            self.output_dir = Path(self.output_dir)
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_file_path = self.output_dir / f"{self.output_file_name}.log"
        
        self.logger = logging.getLogger(self.output_file_name)
        self.logger.setLevel(min(console_level, file_level))
        self.logger.handlers = []   # clean the handlers to avoid repeat handlers
        
        if formatter is None:
            formatter = BasicColorFormatter
        
        # create and add the handler for logging in the console
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setLevel(console_level)
        console_format = formatter(
            f'%(asctime)s | [%(levelname)-{Logger_Level_Name_Size}s] | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        # create and add the handler for writing into the file
        file_handler = logging.FileHandler(filename=output_file_path, encoding='utf-8')
        file_handler.setLevel(file_level)
        file_format = formatter(
            '%(asctime)s | [%(levelname)-8s] | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)
        
        self.number_of_progress_bar = number_of_progress_bars
        self.progress_bar_list: List[tqdm[NoReturn] | None] = [None] * number_of_progress_bars
        
    def log_seperator(self, length: int = 50):
        self.logger.info("=" * length)
        
    def log_debug(self, message: str):
        self.logger.debug(message)
    
    def log_info(self, message: str):
        self.logger.info(message)
        
    def log_success(self, message: str):
        self.logger.info(f"{Fore.GREEN}SUCCESS: {message}{Style.RESET_ALL}")
        
    def log_warning(self, message: str):
        self.logger.warning(message)
        
    def log_error(self, message: str, raise_exception: bool = False):
        self.logger.error(message)
        if raise_exception: raise Exception(message)
        
    def log_critical(self, message: str):
        self.logger.critical(message)
        
    def log_test_assertion(self, assertion_name, result, expected=None, actual=None):
        if result:
            self.logger.info(f"ASSERTION PASSED: {assertion_name}")
        else:
            self.logger.error(f"ASSERTION FAILED: {assertion_name}")
            if expected is not None and actual is not None:
                self.logger.error(f"  Expected: {expected}")
                self.logger.error(f"  Actual: {actual}")
    
    def log_progress(
        self, 
        progress_bar_index: int = 0, 
        description: str = None, 
        total: int = 10, 
        unit: str = "iteration", 
        leave_in_console: bool = True, 
        ncols: int = 100, 
    ):
        if progress_bar_index < 0 or progress_bar_index >= self.number_of_progress_bar:
            raise Exception("Please specified a valid progress_bar_index of the progress bar")
        
        if self.progress_bar_list[progress_bar_index] is None:
            self.progress_bar_list[progress_bar_index] = tqdm(
                total=total, 
                desc="Processing" if description is None else description, 
                unit=unit, 
                leave=leave_in_console, 
                file=sys.stderr,
                ncols=ncols, 
                position=progress_bar_index, 
            )
        elif description is not None:
            self.progress_bar_list[progress_bar_index].set_description(description)
        
        self.progress_bar_list[progress_bar_index].update(1)
        self.progress_bar_list[progress_bar_index].refresh()
        # print() # print the next line to avoid the remaining progress and the next log in the same line
            
    def clear_progress(self, progress_bar_index: int = -1):
        if progress_bar_index == -1:
            for progress_bar in self.progress_bar_list:
                if progress_bar:
                    progress_bar.close()
                    progress_bar = None
            return

        if progress_bar_index < 0 or progress_bar_index >= self.number_of_progress_bar:
            raise Exception("Please specified a valid progress_bar_index of the progress bar")
            
        if self.progress_bar_list[progress_bar_index]:   # clear progress bar if it is exist
            self.progress_bar_list[progress_bar_index].close()
            self.progress_bar_list[progress_bar_index] = None
                