__author__ = 'ict'

import re

from boson.bs_configure import *


class BosonLexicalAnalyzer:
    def __init__(self, filename, ignore=None, error=None):
        self.__token_tuple = []
        if ignore is None:
            self.__ignore = []
        else:
            self.__ignore = set(ignore)
        if error is None:
            self.__error = {invalid_token_class}
        else:
            self.__error = set(error)
        have_invalid = False
        with open(filename, "r") as fp:
            while True:
                line = fp.readline()
                if len(line) == 0:
                    break
                start = -1
                end = -1
                for i in range(len(line)):
                    if start == -1:
                        if line[i] == "\"":
                            start = i + 1
                    else:
                        if line[i] == "\"" and line[i - 1] != "\\":
                            end = i
                            break
                regular_expression = line[start: end]
                line = line[end + 1:]
                while line[0] in [" ", "\t", "\n", "\r"]:
                    line = line[1:]
                while line[-1] in [" ", "\t", "\n", "\r"]:
                    line = line[:-1]
                name = line
                self.__token_tuple.append((name, regular_expression))
                if regular_expression == ".":
                    have_invalid = True
        if not have_invalid:
            self.__token_tuple.append((invalid_token_class, "."))
        self.__token_regular_expression = "|".join("(?P<%s>%s)" % pair for pair in self.__token_tuple)

    def tokenize(self, filename, ignore=None, error=None):
        if ignore is None:
            ignore = self.__ignore
        if error is None:
            error = self.__error
        token_list = []
        with open(filename, "r") as fp:
            text = fp.read()
            for one_token in re.finditer(self.__token_regular_expression, text):
                token_class = one_token.lastgroup
                token_string = one_token.group(token_class)
                if ignore is not None:
                    if token_class in ignore:
                        continue
                if token_class in error:
                    raise Exception("Invalid token: (%s, \"%s\")" % (token_class, token_string))
                token_list.append((token_class, token_string))
            token_list.append((end_symbol, ""))
        return token_list

    def get_token_tuple(self):
        return self.__token_tuple

    def set_ignore(self, ignore):
        self.__ignore == set(ignore)

    def get_ignore(self):
        return self.__ignore

    def set_error(self, error):
        self.__error = set(error)

    def get_error(self):
        return self.__error
