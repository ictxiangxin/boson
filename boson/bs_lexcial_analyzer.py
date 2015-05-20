__author__ = 'ict'

import re

from boson.bs_configure import *


class BosonLexcialAnalyzer:
    def __init__(self, filename):
        token_tuple = []
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
                token_tuple.append((name, regular_expression))
                if regular_expression == ".":
                    have_invalid = True
        if not have_invalid:
            token_tuple.append((invalid_token_class, "."))
        self.__token_regular_expression = "|".join("(?P<%s>%s)" % pair for pair in token_tuple)

    def tokenize(self, filename, ignore=None, error=None):
        token_list = []
        if error is None:
            error = [invalid_token_class]
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
