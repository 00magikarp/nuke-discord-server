import enum
import logging


class CustomLogger:
    class LoggerModes(enum.Enum):
        """
        Custom class to pass enum members into the :func:`log` function.

        Options for the mode are:

        - :attr:`LoggerModes.INFO`
        - :attr:`LoggerModes.WARNING`
        - :attr:`LoggerModes.DEBUG`
        """
        INFO = 1
        WARNING = 2
        DEBUG = 3

    def __init__(self):
        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.DEBUG)

        handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(name)s: %(message)s'))

        self.logger.addHandler(handler)

    def log(self, text: str, logger_mode: LoggerModes) -> None:
        """
        \"Custom\" Logger

        Prints to console and outputs to logger

        :param text: The text to be logged
        :param logger_mode: The mode of logging, from the enum object :class:`LoggerModes`
        """

        match logger_mode:
            case logger_mode.INFO:
                self.logger.info(text)
            case logger_mode.WARNING:
                self.logger.warning(text)
            case logger_mode.DEBUG:
                self.logger.debug(text)
            case _:
                self.logger.warning(f"ATTEMPT TO LOG FAILED. DEFAULTED TO WARNING.")
                self.logger.warning(text)

        print(text)
        return
