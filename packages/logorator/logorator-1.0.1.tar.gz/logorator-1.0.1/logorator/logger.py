from functools import cached_property, wraps
from time import perf_counter
import re
import os


class Logger:
    log_level = 0
    SILENT = False
    OUTPUT_FILE = None

    def __init__(self, silent: bool = None, mode: str = "normal"):
        """
        Initialize the Logger instance.

        Parameters:
            silent (bool, optional): If True, suppresses logging output. Defaults to None,
                                     which uses the global `Logger.SILENT` value.
            mode (str, optional): Determines the logging format.
                                  Options are 'normal' (default) or 'short' (tab-separated).

        Raises:
            TypeError: If `silent` is not a boolean or None.
            ValueError: If `mode` is not one of the supported options ('normal', 'short').

        Example:
            logorator = Logger(silent=False, mode="short")
        """
        if silent is not None and not isinstance(silent, bool):
            raise TypeError("`silent` must be a boolean or None.")
        self.silent = Logger.SILENT if silent is None else silent

        if mode not in {"normal", "short"}:
            raise ValueError("`mode` must be either 'normal' or 'short'.")
        self.mode = mode


    @cached_property
    def eol(self):
        if self.mode == "short":
            return "\t"
        return "\n"

    @staticmethod
    def log(message: str = "", end: str = ""):
        if not isinstance(message, str):
            raise TypeError("`message` must be a string.")
        if not isinstance(end, str):
            raise TypeError("`end` must be a string.")

        try:
            if Logger.OUTPUT_FILE is None:
                print(message, end=end)
            else:
                with open(Logger.OUTPUT_FILE, "a+") as f:
                    sanitized_message = re.sub(r'\033\[[0-9;]*m', "", message)  # Remove ANSI escape codes
                    f.write(sanitized_message + end)
        except IOError as e:
            raise IOError(f"Failed to write to the log file: {Logger.OUTPUT_FILE}. Error: {e}")

    def __call__(self, func):
        """
            Decorator to log the execution of a function, including its arguments and execution time.

            Parameters:
                func (callable): The function to decorate.

            Returns:
                callable: The wrapped function with logging applied.
            """

        @wraps(func)
        def wrapper(*args, **kwargs):
            self.log_level = self.log_level + 1
            print(self.log_level,"<<<<")
            tabs = "  " * (self.log_level - 1)
            start = perf_counter()
            if not self.silent:
                Logger.log(message=f"{tabs}Running \033[32m{func.__name__} \033[0m ", end=self.eol)
                for arg in args:
                    Logger.log(message=f"{tabs}  \33[33m{str(arg)[:1000]}\033[0m", end=self.eol)
                for key in list(kwargs):
                    Logger.log(message=f"{tabs}  {key}: \33[33m{str(kwargs[key])[:1000]}\033[0m", end=self.eol)

            result = func(*args, **kwargs)
            end = perf_counter()
            duration = '{:,.2f}'.format((end - start) * 1000)
            if not self.silent:
                Logger.log(
                    message=f"{tabs}Finished \033[32m{func.__name__} \033[0m Time elapsed: \033[32m{duration} ms\033[0m",
                    end=self.eol)
            self.log_level = self.log_level - 1
            return result

        return wrapper

    @staticmethod
    def set_silent(silent: bool = True):
        """
        Set the global silent mode for the Logger.

        Parameters:
            silent (bool): If True, suppresses all logging output globally. Defaults to True.
        """
        if not isinstance(silent, bool):
            raise TypeError("`silent` must be a boolean.")

        Logger.SILENT = silent

    @staticmethod
    def set_output(filename: str | None = None):
        """
        Set the global output file for the Logger.

        Parameters:
            filename (str | None): The name of the file to write logs to. If None, logs are written to the console.
        """
        if filename is not None and not isinstance(filename, str):
            raise TypeError("`filename` must be a string or None.")

        if filename is not None:
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                try:
                    os.makedirs(directory, exist_ok=True)
                except OSError as e:
                    raise OSError(f"Failed to create directory `{directory}` for log file: {e}")

            try:
                with open(filename, "a+") as f:
                    pass
            except IOError as e:
                raise IOError(f"Failed to open log file `{filename}` for writing: {e}")

        Logger.OUTPUT_FILE = filename

    @staticmethod
    def note(note: str = "", mode: str = "normal"):
        """
        Log a custom note with the current logging level's indentation.

        Parameters:
            note (str): The custom message to log. Defaults to an empty string.
            mode (str): The logging mode. Options are:
                - "normal": Each note ends with a newline.
                - "short": Each note ends with a tab character (\t).
                Defaults to "normal".
        """
        if not isinstance(note, str):
            raise TypeError("`note` must be a string.")
        if mode not in {"normal", "short"}:
            raise ValueError("`mode` must be either 'normal' or 'short'.")

        if Logger.SILENT:
            return

        Logger.log(
            f"\033[34m{note} \033[0m",
            end=("\t" if mode == "short" else "\n")
        )
