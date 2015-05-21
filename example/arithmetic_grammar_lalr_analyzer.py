"""
    Boson v0.3
    By: ict
    Email: ictxiangxin@gmail.com

    This code generated by boson python code generator.
"""


import re


boson_token_tuple = [
    ("int",           r"[1-9][0-9]*"),
    ("float",         r"[1-9][0-9]*\.[0-9]+"),
    ("plus",          r"\+"),
    ("minus",         r"\-"),
    ("times",         r"\*"),
    ("dive",          r"\/"),
    ("power",         r"\^"),
    ("bl",            r"\("),
    ("br",            r"\)"),
    ("boson_invalid", r"."),
]

boson_ignore = {
}

boson_error = {
    "boson_invalid",
}

boson_token_regular_expression = "|".join("(?P<%s>%s)" % pair for pair in boson_token_tuple)


terminal_index = {
    "float":    0,
    "int":      1,
    "literal1": 2,
    "literal2": 3,
    "literal3": 4,
    "literal4": 5,
    "literal5": 6,
    "literal6": 7,
    "literal7": 8,
    "$":        9,
}

action_table = [
    ["s6",  "s7",  "e",   "e",   "e",   "e",   "e",   "s2",  "e",   "e"],
    ["e",   "e",   "r9",  "r9",  "r9",  "r9",  "s9",  "e",   "r9",  "e"],
    ["s6",  "s7",  "e",   "e",   "e",   "e",   "e",   "s2",  "e",   "e"],
    ["e",   "e",   "r12", "r12", "r12", "r12", "r12", "e",   "r12", "e"],
    ["e",   "e",   "r4",  "r4",  "s12", "s11", "e",   "e",   "r4",  "e"],
    ["e",   "e",   "r5",  "r5",  "r5",  "r5",  "r5",  "e",   "r5",  "e"],
    ["e",   "e",   "r7",  "r7",  "r7",  "r7",  "r7",  "e",   "r7",  "e"],
    ["e",   "e",   "r8",  "r8",  "r8",  "r8",  "r8",  "e",   "r8",  "e"],
    ["e",   "e",   "s13", "s14", "e",   "e",   "e",   "e",   "e",   "a"],
    ["s6",  "s7",  "e",   "e",   "e",   "e",   "e",   "s2",  "e",   "e"],
    ["e",   "e",   "s13", "s14", "e",   "e",   "e",   "e",   "s16", "e"],
    ["s6",  "s7",  "e",   "e",   "e",   "e",   "e",   "s2",  "e",   "e"],
    ["s6",  "s7",  "e",   "e",   "e",   "e",   "e",   "s2",  "e",   "e"],
    ["s6",  "s7",  "e",   "e",   "e",   "e",   "e",   "s2",  "e",   "e"],
    ["s6",  "s7",  "e",   "e",   "e",   "e",   "e",   "s2",  "e",   "e"],
    ["e",   "e",   "r6",  "r6",  "r6",  "r6",  "r6",  "e",   "r6",  "e"],
    ["e",   "e",   "r1",  "r1",  "r1",  "r1",  "r1",  "e",   "r1",  "e"],
    ["e",   "e",   "r11", "r11", "r11", "r11", "s9",  "e",   "r11", "e"],
    ["e",   "e",   "r10", "r10", "r10", "r10", "s9",  "e",   "r10", "e"],
    ["e",   "e",   "r2",  "r2",  "s12", "s11", "e",   "e",   "r2",  "e"],
    ["e",   "e",   "r3",  "r3",  "s12", "s11", "e",   "e",   "r3",  "e"],
]

non_terminal_index = {
    "D": 0,
    "E": 1,
    "F": 2,
    "N": 3,
    "T": 4,
}

goto_table = [
    [5,  8,  1,  3,   4],
    [-1, -1, -1, -1, -1],
    [5,  10, 1,  3,   4],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [15, -1, -1, 3,  -1],
    [-1, -1, -1, -1, -1],
    [5,  -1, 17, 3,  -1],
    [5,  -1, 18, 3,  -1],
    [5,  -1, 1,  3,  19],
    [5,  -1, 1,  3,  20],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
]

reduce_symbol_sum = {
    0:  1,
    1:  3,
    2:  3,
    3:  3,
    4:  1,
    5:  1,
    6:  3,
    7:  1,
    8:  1,
    9:  1,
    10: 3,
    11: 3,
    12: 1,
}

reduce_to_non_terminal = {
    0:  "start",
    1:  "D",
    2:  "E",
    3:  "E",
    4:  "E",
    5:  "F",
    6:  "F",
    7:  "N",
    8:  "N",
    9:  "T",
    10: "T",
    11: "T",
    12: "D",
}

literal_map = {
    "/": "literal4",
    ")": "literal7",
    "*": "literal3",
    "^": "literal5",
    "-": "literal2",
    "+": "literal1",
    "(": "literal6",
}


def boson_lexical_analysis(text):
    boson_token_list = []
    for one_token in re.finditer(boson_token_regular_expression, text):
        token_class = one_token.lastgroup
        token_text = one_token.group(token_class)
        if token_class in boson_ignore:
            continue
        if token_class in boson_error:
            raise Exception("Invalid token: (%s, \"%s\")" % (token_class, token_text))
        boson_token_list.append((token_class, token_text))
    boson_token_list.append(("$", ""))
    return boson_token_list


def boson_grammar_analysis(token_list):
    boson_stack = []
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
            boson_stack.append(token)
        elif operation_flag == "r":
            operation_number = int(operation[1:])
            reduce_sum = reduce_symbol_sum[operation_number]
            for _ in range(reduce_sum):
                stack.pop()
            now_state = stack[-1]
            now_non_terminal_index = non_terminal_index[reduce_to_non_terminal[operation_number]]
            stack.append(goto_table[now_state][now_non_terminal_index])
            if operation_number == 0:
                # start -> E
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, boson_stack.pop())
                boson_reduce = boson_sentence[0]
                boson_stack.append(boson_reduce)
            elif operation_number == 1:
                # D -> '(' E ')'
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, boson_stack.pop())
                boson_reduce = [boson_sentence[1]]
                boson_stack.append(boson_reduce)
            elif operation_number == 2:
                # E -> E '+' T
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, boson_stack.pop())
                boson_reduce = [boson_sentence[1], boson_sentence[0], boson_sentence[2]]
                boson_stack.append(boson_reduce)
            elif operation_number == 3:
                # E -> E '-' T
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, boson_stack.pop())
                boson_reduce = [boson_sentence[1], boson_sentence[0], boson_sentence[2]]
                boson_stack.append(boson_reduce)
            elif operation_number == 4:
                # E -> T
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, boson_stack.pop())
                boson_reduce = boson_sentence[0]
                boson_stack.append(boson_reduce)
            elif operation_number == 5:
                # F -> D
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, boson_stack.pop())
                boson_reduce = boson_sentence[0]
                boson_stack.append(boson_reduce)
            elif operation_number == 6:
                # F -> F '^' D
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, boson_stack.pop())
                boson_reduce = [boson_sentence[1], boson_sentence[0], boson_sentence[2]]
                boson_stack.append(boson_reduce)
            elif operation_number == 7:
                # N -> float
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, boson_stack.pop())
                boson_reduce = boson_sentence[0]
                boson_stack.append(boson_reduce)
            elif operation_number == 8:
                # N -> int
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, boson_stack.pop())
                boson_reduce = boson_sentence[0]
                boson_stack.append(boson_reduce)
            elif operation_number == 9:
                # T -> F
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, boson_stack.pop())
                boson_reduce = boson_sentence[0]
                boson_stack.append(boson_reduce)
            elif operation_number == 10:
                # T -> T '*' F
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, boson_stack.pop())
                boson_reduce = [boson_sentence[1], boson_sentence[0], boson_sentence[2]]
                boson_stack.append(boson_reduce)
            elif operation_number == 11:
                # T -> T '/' F
                boson_sentence = []
                for boson_i in range(3):
                    boson_sentence.insert(0, boson_stack.pop())
                boson_reduce = [boson_sentence[1], boson_sentence[0], boson_sentence[2]]
                boson_stack.append(boson_reduce)
            elif operation_number == 12:
                # D -> N
                boson_sentence = []
                for boson_i in range(1):
                    boson_sentence.insert(0, boson_stack.pop())
                boson_reduce = boson_sentence[0]
                boson_stack.append(boson_reduce)
            else:
                raise Exception("Invalid reduce number: %d" % operation_number)
        elif operation_flag == "a":
            return boson_stack[0]
        else:
            raise Exception("Invalid action: %s" % operation)
