__author__ = 'ict'

import re

start_non_terminal_symbol = "start"

token_tuple = [
    ("ROOT", r"root"),
    ("NAME", r"[_a-zA-Z]+"),
    ("TOWARD", r"\->"),
    ("OR", r"\|"),
    ("SKIP", r"[ \t]+"),
    ("NEWLINE", r"\n|\r\n"),
    ("INVALID", r"."),
]
token_regrex = "|".join("(?P<%s>%s)" % pair for pair in token_tuple)

terminal_index = {
    "NAME":   0,
    "TOWARD": 1,
    "OR":     2,
    "$":      3,
}

action_table = [
    ["s1", "e",  "e",  "e"],
    ["s2", "s5", "r4", "r4"],
    ["s2", "e",  "r4", "r4"],
    ["e",  "e",  "r3", "r3"],
    ["e",  "e",  "s7", "r2"],
    ["s2", "e",  "e",  "e"],
    ["e",  "e",  "e",  "a"],
    ["s2", "e",  "e",  "e"],
    ["e",  "e",  "e",  "r1"],
]

non_terminal_index = {
    "N": 0,
    "L": 1,
}

goto_table = [
    [4, -1],
    [3, -1],
    [3, -1],
    [-1, -1],
    [-1, -1],
    [4,  6],
    [-1, -1],
    [4, 8],
    [-1, -1],
]


def bs_token_list(filename):
    with open(filename, "r") as fp:
        text = fp.read()
        token_list = list()
        line_number = 1
        temp_list = list()
        for one_token in re.finditer(token_regrex, text):
            token_class = one_token.lastgroup
            token_string = one_token.group(token_class)
            if token_class == "SKIP":
                pass
            elif token_class == "NEWLINE":
                temp_list.append(("$", ""))
                token_list.append(temp_list)
                temp_list = list()
                line_number += 1
            elif token_class == "INVALID":
                raise RuntimeError("[Line: %d] Invalid token: %s" % (line_number, token_string))
            else:
                temp_list.append((token_class, token_string))
        if len(temp_list) != 0:
            temp_list.append(("$", ""))
            token_list.append(temp_list)
    return token_list


def bs_grammar_analysis(token_list):
    sentense_set = set()
    for line in token_list:
        stack = [0]
        symbol_stack = []
        token_index = 0
        while token_index < len(line):
            token = line[token_index]
            op = action_table[stack[-1]][terminal_index[token[0]]]
            if op[0] == "e":
                raise Exception("Grammar error: " + " ".join([e[1] for e in line]))
            elif op[0] == "s":
                stack.append(int(op[1:]))
                if token[0] == "NAME":
                    symbol_stack.append(token)
                token_index += 1
            elif op[0] == "r":
                reduce_number = int(op[1:])
                if reduce_number == 1:
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.append(goto_table[stack[-1]][non_terminal_index["L"]])
                elif reduce_number == 2:
                    stack.pop()
                    stack.append(goto_table[stack[-1]][non_terminal_index["L"]])
                elif reduce_number == 3:
                    stack.pop()
                    stack.pop()
                    stack.append(goto_table[stack[-1]][non_terminal_index["N"]])
                    non_terminal_n = symbol_stack.pop()
                    non_terminal_n.append(symbol_stack.pop())
                    symbol_stack.append(non_terminal_n)
                elif reduce_number == 4:
                    stack.pop()
                    stack.append(goto_table[stack[-1]][non_terminal_index["N"]])
                    symbol_stack.append([symbol_stack.pop()])
                else:
                    raise Exception("Invalid reduce number: %d" % reduce_number)
            elif op[0] == "a":
                temp_sentense_set = set()
                for sentense in symbol_stack[1:]:
                    sentense.reverse()
                    temp_sentense_set.add(tuple([symbol_stack[0][1]] + [e[1] for e in sentense]))
                sentense_set |= temp_sentense_set
                break
    if start_non_terminal_symbol not in set([sentence[0] for sentence in sentense_set]):
        raise Exception("No start non terminal symbol in grammar, need: %s" % start_non_terminal_symbol)
    return sentense_set