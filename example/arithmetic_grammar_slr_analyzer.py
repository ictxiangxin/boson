"""
    Boson v0.5
    By: ict
    Email: ictxiangxin@gmail.com

    This code generated by boson python code generator.
"""


import re


boson_token_tuple = [
    ("int",           r"[1-9][0-9]*"),
    ("plus",          r"\+"),
    ("minus",         r"\-"),
    ("times",         r"\*"),
    ("dive",          r"\/"),
    ("power",         r"\^"),
    ("bl",            r"\("),
    ("br",            r"\)"),
    ("skip",          r"\t|\ "),
    ("boson_invalid", r"."),
]

boson_ignore = {
    "skip",
}

boson_error = {
    "boson_invalid",
}

boson_token_regular_expression = "|".join("(?P<%s>%s)" % pair for pair in boson_token_tuple)


terminal_index = {
    "literal6": 0,
    "literal7": 1,
    "literal3": 2,
    "literal1": 3,
    "literal2": 4,
    "literal4": 5,
    "literal5": 6,
    "int":      7,
    "$":        8,
}

action_table = [
    ["s2",  "e",   "e",   "e",   "e",   "e",   "e",   "s6",    "e"],
    ["e",   "r8",  "r8",  "r8",  "r8",  "r8",  "s7",  "e",    "r8"],
    ["s2",  "e",   "e",   "e",   "e",   "e",   "e",   "s6",    "e"],
    ["e",   "r5",  "r5",  "r5",  "r5",  "r5",  "r5",  "e",    "r5"],
    ["e",   "r4",  "s10", "r4",  "r4",  "s9",  "e",   "e",    "r4"],
    ["e",   "e",   "e",   "s11", "s12", "e",   "e",   "e",     "a"],
    ["e",   "r1",  "r1",  "r1",  "r1",  "r1",  "r1",  "e",    "r1"],
    ["s2",  "e",   "e",   "e",   "e",   "e",   "e",   "s6",    "e"],
    ["e",   "s14", "e",   "s11", "s12", "e",   "e",   "e",     "e"],
    ["s2",  "e",   "e",   "e",   "e",   "e",   "e",   "s6",    "e"],
    ["s2",  "e",   "e",   "e",   "e",   "e",   "e",   "s6",    "e"],
    ["s2",  "e",   "e",   "e",   "e",   "e",   "e",   "s6",    "e"],
    ["s2",  "e",   "e",   "e",   "e",   "e",   "e",   "s6",    "e"],
    ["e",   "r6",  "r6",  "r6",  "r6",  "r6",  "r6",  "e",    "r6"],
    ["e",   "r7",  "r7",  "r7",  "r7",  "r7",  "r7",  "e",    "r7"],
    ["e",   "r10", "r10", "r10", "r10", "r10", "s7",  "e",   "r10"],
    ["e",   "r9",  "r9",  "r9",  "r9",  "r9",  "s7",  "e",    "r9"],
    ["e",   "r2",  "s10", "r2",  "r2",  "s9",  "e",   "e",    "r2"],
    ["e",   "r3",  "s10", "r3",  "r3",  "s9",  "e",   "e",    "r3"],
]

non_terminal_index = {
    "D": 0,
    "E": 1,
    "F": 2,
    "T": 3,
}

goto_table = [
    [3,  5,  1,   4],
    [-1, -1, -1, -1],
    [3,  8,  1,   4],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
    [13, -1, -1, -1],
    [-1, -1, -1, -1],
    [3,  -1, 15, -1],
    [3,  -1, 16, -1],
    [3,  -1, 1,  17],
    [3,  -1, 1,  18],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
]

reduce_symbol_sum = {
    0:  1,
    1:  1,
    2:  3,
    3:  3,
    4:  1,
    5:  1,
    6:  3,
    7:  3,
    8:  1,
    9:  3,
    10: 3,
}

reduce_to_non_terminal = {
    0:  "S",
    1:  "D",
    2:  "E",
    3:  "E",
    4:  "E",
    5:  "F",
    6:  "F",
    7:  "D",
    8:  "T",
    9:  "T",
    10: "T",
}

literal_map = {
    "/": "literal4",
    "^": "literal5",
    "(": "literal6",
    ")": "literal7",
    "*": "literal3",
    "+": "literal1",
    "-": "literal2",
}


def calculate_tokenize(text):
    boson_token_list = []
    for one_token in re.finditer(boson_token_regular_expression, text):
        token_class = one_token.lastgroup
        token_text = one_token.group(token_class)
        if token_class in boson_ignore:
            continue
        elif token_class in boson_error:
            raise Exception("Invalid token: (%s, \"%s\")" % (token_class, token_text))
        else:
            boson_token_list.append((token_class, token_text))
    boson_token_list.append(("$", ""))
    return boson_token_list


def simple_calculate(token_list):
    symbol_stack = []
    stack = [0]
    token_index = 0
    while token_index < len(token_list):
        token = token_list[token_index]
        if token[1] in literal_map:
            token_type = literal_map[token[1]]
        else:
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
            symbol_stack.append(token)
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
                # S -> E
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = boson_sentence[0]
                symbol_stack.append(boson_reduce)
            elif operation_number == 1:
                # D -> int
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = boson_sentence[0][1]
                symbol_stack.append(boson_reduce)
            elif operation_number == 2:
                # E -> E + T
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = [boson_sentence[1][1], boson_sentence[0], boson_sentence[2]]
                symbol_stack.append(boson_reduce)
            elif operation_number == 3:
                # E -> E - T
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = [boson_sentence[1][1], boson_sentence[0], boson_sentence[2]]
                symbol_stack.append(boson_reduce)
            elif operation_number == 4:
                # E -> T
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = boson_sentence[0]
                symbol_stack.append(boson_reduce)
            elif operation_number == 5:
                # F -> D
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = boson_sentence[0]
                symbol_stack.append(boson_reduce)
            elif operation_number == 6:
                # F -> F ^ D
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = [boson_sentence[1][1], boson_sentence[0], boson_sentence[2]]
                symbol_stack.append(boson_reduce)
            elif operation_number == 7:
                # D -> ( E )
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = boson_sentence[1]
                symbol_stack.append(boson_reduce)
            elif operation_number == 8:
                # T -> F
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = boson_sentence[0]
                symbol_stack.append(boson_reduce)
            elif operation_number == 9:
                # T -> T * F
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = [boson_sentence[1][1], boson_sentence[0], boson_sentence[2]]
                symbol_stack.append(boson_reduce)
            elif operation_number == 10:
                # T -> T / F
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, symbol_stack.pop())
                boson_reduce = [boson_sentence[1][1], boson_sentence[0], boson_sentence[2]]
                symbol_stack.append(boson_reduce)
            else:
                raise Exception("Invalid reduce number: %d" % operation_number)
        elif operation_flag == "a":
            break
        else:
            raise Exception("Invalid action: %s" % operation)
    return symbol_stack[0]


expr = input("expression: ")
expr_token = calculate_tokenize(expr)
print(simple_calculate(expr_token))
