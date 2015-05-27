__author__ = 'ict'

import re

from boson.bs_configure import *


token_tuple = [
    ("name",         r"[_a-zA-Z][_a-zA-Z0-9]*"),
    ("string",       r"\".*?[^\\]\"|\"\""),
    ("command",      r"%[_a-zA-Z]+"),
    ("end",          r";"),
    ("skip",         r"[ \t]+"),
    ("newline",      r"\\r\n|\n"),
    ("invalid",      r"."),
]

token_regular_expression = "|".join("(?P<%s>%s)" % pair for pair in token_tuple)


terminal_index = {
    "command": 0,
    "end":     1,
    "name":    2,
    "string":  3,
    "$":       4,
}

action_table = [
    ["s4",  "e",   "s3",  "s5",   "e"],
    ["r5",  "e",   "r5",  "r5",  "r5"],
    ["r6",  "e",   "r6",  "r6",  "r6"],
    ["e",   "e",   "e",   "s8",   "e"],
    ["e",   "e",   "s10", "e",    "e"],
    ["e",   "e",   "s11", "e",    "e"],
    ["s4",  "e",   "s3",  "s5",   "a"],
    ["r1",  "e",   "r1",  "r1",  "r1"],
    ["e",   "s13", "e",   "e",    "e"],
    ["e",   "s14", "s15", "e",    "e"],
    ["e",   "r7",  "r7",  "e",    "e"],
    ["e",   "s16", "e",   "e",    "e"],
    ["r9",  "e",   "r9",  "r9",  "r9"],
    ["r3",  "e",   "r3",  "r3",  "r3"],
    ["r2",  "e",   "r2",  "r2",  "r2"],
    ["e",   "r8",  "r8",  "e",    "e"],
    ["r4",  "e",   "r4",  "r4",  "r4"],
]

non_terminal_index = {
    "block":        0,
    "command_line": 1,
    "lexical_line": 2,
    "line":         3,
    "name_list":    4,
}

goto_table = [
    [6,  1,  2,  7,  -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1,  9],
    [-1, -1, -1, -1, -1],
    [-1, 1,  2,  12, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
]

reduce_symbol_sum = {
    0:  1,
    1:  1,
    2:  3,
    3:  3,
    4:  3,
    5:  1,
    6:  1,
    7:  1,
    8:  2,
    9:  2,
}

reduce_to_non_terminal = {
    0:  "start",
    1:  "block",
    2:  "command_line",
    3:  "lexical_line",
    4:  "lexical_line",
    5:  "line",
    6:  "line",
    7:  "name_list",
    8:  "name_list",
    9:  "block",
}


class BosonLexicalAnalyzer:
    def __init__(self, filename, ignore=None, error=None):
        self.__token_tuple = []
        self.__skip_type = set()
        self.__invalid_type = set()
        if ignore is None:
            self.__ignore = set()
        else:
            self.__ignore = set(ignore)
        if error is None:
            self.__error = {invalid_token_class}
        else:
            self.__error = set(error)
        token_list = []
        have_invalid = False
        with open(filename, "r") as fp:
            text = fp.read()
            for one_token in re.finditer(token_regular_expression, text):
                token_class = one_token.lastgroup
                token_string = one_token.group(token_class)
                if token_class in ["skip", "newline"]:
                    pass
                elif token_class == "invalid":
                    raise RuntimeError("Invalid token: %s" % token_string)
                else:
                    token_list.append((token_class, token_string))
        symbol_stack = []
        stack = [0]
        token_index = 0
        while token_index < len(token_list):
            token = token_list[token_index]
            token_type = token[0]
            now_state = stack[-1]
            operation = action_table[now_state][terminal_index[token_type]]
            operation_flag = operation[0]
            if operation_flag == "e":
                raise Exception("Grammar error: " + " ".join([t[1] for t in token_list]))
            elif operation_flag == "s":
                operation_number = int(operation[1:])
                stack.append(operation_number)
                token_index += 1
                if token_type in ["name", "string", "command"]:
                    symbol_stack.append(token[1])
            elif operation_flag == "r":
                operation_number = int(operation[1:])
                reduce_sum = reduce_symbol_sum[operation_number]
                for _ in range(reduce_sum):
                    stack.pop()
                now_state = stack[-1]
                now_non_terminal_index = non_terminal_index[reduce_to_non_terminal[operation_number]]
                goto_next_state = goto_table[now_state][now_non_terminal_index]
                if goto_next_state == -1:
                    raise Exception("Invalid goto action: state=%d, non-terminal=%d" % (now_state, now_non_terminal_index))
                stack.append(goto_table[now_state][now_non_terminal_index])
                if operation_number == 0:
                    pass
                elif operation_number == 1:
                    pass
                elif operation_number == 2:
                    name_list = symbol_stack.pop()
                    command = symbol_stack.pop()
                    if command == "%ignore":
                        self.__ignore |= set(name_list)
                    elif command == "%error":
                        self.__error |= set(name_list)
                    else:
                        raise Exception("Invalid command: %s" % command)
                elif operation_number == 3:
                    string = symbol_stack.pop()
                    name = symbol_stack.pop()
                    if string == ".":
                        have_invalid = True
                    self.__token_tuple.append((name, string[1: -1]))
                elif operation_number == 4:
                    name = symbol_stack.pop()
                    string = symbol_stack.pop()
                    if string == ".":
                        have_invalid = True
                    self.__token_tuple.append((name, string[1: -1]))
                    pass
                elif operation_number == 5:
                    pass
                elif operation_number == 6:
                    pass
                elif operation_number == 7:
                    name = symbol_stack.pop()
                    symbol_stack.append([name])
                elif operation_number == 8:
                    name = symbol_stack.pop()
                    name_list = symbol_stack.pop()
                    symbol_stack.append(name_list + [name])
                elif operation_number == 9:
                    pass
                else:
                    raise Exception("Invalid reduce number: %d" % operation_number)
            elif operation_flag == "a":
                break
            else:
                raise Exception("Invalid action: %s" % operation)
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
