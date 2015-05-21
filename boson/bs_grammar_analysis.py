__author__ = 'ict'

import re

from boson.bs_configure import *

token_tuple = [
    ("name",    r"[_a-zA-Z][_a-zA-Z0-9]*"),
    ("reduce",  r"\:"),
    ("or",      r"\|"),
    ("code",    r"\{.*\}"),
    ("literal", r"\'[^\']+\'"),
    ("end",     r"\;"),
    ("skip",    r"[ \t]+"),
    ("newline", r"\n|\r\n"),
    ("invalid", r"."),
]

token_regular_expression = "|".join("(?P<%s>%s)" % pair for pair in token_tuple)

terminal_index = {
    "name":   0,
    "reduce": 1,
    "end":    2,
    "code":   3,
    "or":     4,
    "$":      5,
}

action_table = [
    ["s1",  "e",   "e",   "e",   "e",    "e"],
    ["e",   "s4",  "e",   "e",   "e",    "e"],
    ["r1",  "e",   "e",   "e",   "e",   "r1"],
    ["s1",  "e",   "e",   "e",   "e",    "a"],
    ["s8",  "e",   "e",   "e",   "e",    "e"],
    ["r4",  "e",   "e",   "e",   "e",   "r4"],
    ["e",   "e",   "s10", "e",   "s11",  "e"],
    ["e",   "e",   "r8",  "e",   "r8",   "e"],
    ["r2",  "e",   "r2",  "r2",  "r2",   "e"],
    ["s12", "e",   "r5",  "s13", "r5",   "e"],
    ["r7",  "e",   "e",   "e",   "e",   "r7"],
    ["s8",  "e",   "e",   "e",   "e",    "e"],
    ["r3",  "e",   "r3",  "r3",  "r3",   "e"],
    ["e",   "e",   "r6",  "e",   "r6",   "e"],
    ["e",   "e",   "r9",  "e",   "r9",   "e"],
]

non_terminal_index = {
    "statement_block": 0,
    "statement_set":   1,
    "name_list":       2,
    "statement":       3,
    "grammar":         4,
}

goto_table = [
    [2,  -1, -1, -1,  3],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [5,  -1, -1, -1, -1],
    [-1, 6,  9,  7,  -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, 9,  14, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
]

reduce_symbol_sum = {
    0:  1,
    1:  1,
    2:  1,
    3:  2,
    4:  2,
    5:  1,
    6:  2,
    7:  4,
    8:  1,
    9:  3,
}

reduce_to_non_terminal = {
    0:  "start",
    1:  "grammar",
    2:  "name_list",
    3:  "name_list",
    4:  "grammar",
    5:  "statement",
    6:  "statement",
    7:  "statement_block",
    8:  "statement_set",
    9:  "statement_set",
}


def bs_token_list(filename):
    with open(filename, "r") as fp:
        text = fp.read()
        token_list = list()
        literal_map = {}
        literal_reverse_map = {}
        line_number = 1
        literal_number = 1
        for one_token in re.finditer(token_regular_expression, text):
            token_class = one_token.lastgroup
            token_string = one_token.group(token_class)
            if token_class == "skip":
                pass
            elif token_class == "newline":
                line_number += 1
            elif token_class == "invalid":
                raise RuntimeError("[Line: %d] Invalid token: %s" % (line_number, token_string))
            elif token_class == "literal":
                literal_string = token_string[1: -1]
                if literal_string in literal_map:
                    literal_class = literal_map[literal_string]
                else:
                    literal_class = literal_templet % literal_number
                    literal_number += 1
                    literal_map[literal_string] = literal_class
                    literal_reverse_map[literal_class] = literal_string
                token_list.append(("name", literal_class))
            else:
                token_list.append((token_class, token_string))
    token_list.append((end_symbol, ""))
    return token_list, (literal_map, literal_reverse_map)


def bs_grammar_analyzer(token_list):
    sentence_set = set()
    reduce_code = {}
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
            if token[0] in ["name", "code"]:
                symbol_stack.append(token)
        elif operation_flag == "r":
            operation_number = int(operation[1:])
            reduce_sum = reduce_symbol_sum[operation_number]
            for _ in range(reduce_sum):
                stack.pop()
            now_state = stack[-1]
            stack.append(goto_table[now_state][non_terminal_index[reduce_to_non_terminal[operation_number]]])
            if operation_number == 1:
                pass
            elif operation_number == 2:
                symbol_stack.append([symbol_stack.pop()])
            elif operation_number == 3:
                name = symbol_stack.pop()
                name_list = symbol_stack.pop()
                name_list.append(name)
                symbol_stack.append(name_list)
            elif operation_number == 4:
                pass
            elif operation_number == 5:
                name_list = symbol_stack.pop()
                symbol_stack.append((name_list, None))
            elif operation_number == 6:
                code = symbol_stack.pop()
                name_list = symbol_stack.pop()
                symbol_stack.append((name_list, code))
            elif operation_number == 7:
                statement_set = symbol_stack.pop()
                name = symbol_stack.pop()
                for statement in statement_set:
                    temp_statement = [name] + statement[0]
                    sentence = tuple([token[1] for token in temp_statement])
                    sentence_set.add(sentence)
                    if statement[1] is not None:
                        reduce_code[sentence] = statement[1][1]
                    else:
                        reduce_code[sentence] = None
            elif operation_number == 8:
                statement = symbol_stack.pop()
                symbol_stack.append([statement])
            elif operation_number == 9:
                statement = symbol_stack.pop()
                statement_set = symbol_stack.pop()
                symbol_stack.append(statement_set + [statement])
            else:
                raise Exception("Invalid reduce number: %d" % operation_number)
        elif operation_flag == "a":
            break
        else:
            raise Exception("Invalid action: %s" % operation)
    return sentence_set, reduce_code


def bs_grammar_analysis(filename):
    token_list, literal = bs_token_list(filename)
    sentence_set, reduce_code = bs_grammar_analyzer(token_list)
    return sentence_set, reduce_code, literal
