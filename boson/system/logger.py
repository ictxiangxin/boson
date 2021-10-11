import os
import time
from enum import Enum
from typing import Optional, TextIO

import boson.configure as configure


class LogLevel(Enum):
    error = 'Error'
    warning = 'Warning'
    info = 'Info'
    debug = 'Debug'


class Logger:
    def __init__(self):
        self.__file_path: str = ''
        self.__file_name: str = ''
        self.__log_file: Optional[TextIO] = None

    def __del__(self):
        self.close()

    def initialize(self, file_path: str = None, file_name: str = None):
        if file_path is None:
            self.__file_path = configure.boson_log_file_default_path
        else:
            self.__file_path: str = file_path
        if file_name is None:
            self.generate_log_file_name()
        else:
            self.__file_name: str = file_name
        if not os.path.isdir(self.__file_path):
            os.mkdir(self.__file_path)
        self.__log_file: TextIO = open(os.path.join(self.__file_path, self.__file_name), 'w', encoding=configure.boson_default_encoding)

    def close(self):
        if self.__log_file is not None and not self.__log_file.closed:
            self.__log_file.close()

    def generate_log_file_name(self):
        self.__file_name: str = configure.boson_name + '_' + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + '.log'

    def log(self, text: str, level: LogLevel):
        log_head = '[{}]'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        log_level = '<{}>'.format(level.value)
        self.__log_file.write('{} {} {}\n'.format(log_head, log_level, text))

    def log_block(self, block_text: str, level: LogLevel):
        log_head = '[{}] <{}>\n'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), level.value)
        log_block_start = '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
        log_block_end = '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'
        self.__log_file.writelines([log_head, log_block_start, block_text, log_block_end])

    def error(self, text: str):
        self.log(text, LogLevel.error)

    def warning(self, text: str):
        self.log(text, LogLevel.warning)

    def info(self, text: str):
        self.log(text, LogLevel.info)

    def debug(self, text: str):
        self.log(text, LogLevel.debug)

    def error_block(self, block_text: str):
        self.log_block(block_text, LogLevel.error)

    def warning_block(self, block_text: str):
        self.log_block(block_text, LogLevel.warning)

    def info_block(self, block_text: str):
        self.log_block(block_text, LogLevel.info)

    def debug_block(self, block_text: str):
        self.log_block(block_text, LogLevel.debug)


logger = Logger()
