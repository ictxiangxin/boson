__author__ = 'ict'

import re

from boson.bs_configure import *

token_tuple = [
    ("name",    r"[_a-zA-Z][_a-zA-Z0-9]*"),
    ("reduce",  r"\:"),
    ("or",      r"\|"),
    ("code",    r"\{.*\}"),
    ("literal", r"\'[^\']+\'"),
    ("comment", r"#[^(\r\n|\n)]*"),
    ("command", r"%[_a-zA-Z]+"),
    ("end",     r"\;"),
    ("skip",    r"[ \t]+"),
    ("newline", r"\n|\r\n"),
    ("invalid", r"."),
]

token_regular_expression = "|".join("(?P<%s>%s)" % pair for pair in token_tuple)

terminal_index = {
    "code":    0,
    "command": 1,
    "end":     2,
    "name":    3,
    "or":      4,
    "reduce":  5,
    "$":       6,
}

action_table = [
    ["e",   "s4",  "e",   "s7",  "e",   "e",     "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",     "a"],
    ["e",   "s4",  "e",   "s7",  "e",   "e",     "e"],
    ["e",   "e",   "e",   "r12", "e",   "e",   "r12"],
    ["e",   "e",   "e",   "s11", "e",   "e",     "e"],
    ["e",   "e",   "e",   "s7",  "e",   "e",    "r8"],
    ["e",   "r1",  "e",   "r1",  "e",   "e",     "e"],
    ["e",   "e",   "e",   "e",   "e",   "s13",   "e"],
    ["e",   "r14", "e",   "r14", "e",   "e",     "e"],
    ["e",   "e",   "e",   "s7",  "e",   "e",    "r7"],
    ["e",   "e",   "s14", "s15", "e",   "e",     "e"],
    ["r9",  "e",   "r9",  "r9",  "r9",  "e",     "e"],
    ["e",   "e",   "e",   "r13", "e",   "e",   "r13"],
    ["e",   "e",   "e",   "s11", "e",   "e",     "e"],
    ["e",   "r2",  "e",   "r2",  "e",   "e",     "e"],
    ["r10", "e",   "r10", "r10", "r10", "e",     "e"],
    ["s19", "e",   "r3",  "s15", "r3",  "e",     "e"],
    ["e",   "e",   "s21", "e",   "s20", "e",     "e"],
    ["e",   "e",   "r5",  "e",   "r5",  "e",     "e"],
    ["e",   "e",   "r4",  "e",   "r4",  "e",     "e"],
    ["e",   "e",   "e",   "s11", "e",   "e",     "e"],
    ["e",   "e",   "e",   "r11", "e",   "e",   "r11"],
    ["e",   "e",   "r6",  "e",   "r6",  "e",     "e"],
]

non_terminal_index = {
    "command_block":   0,
    "command_line":    1,
    "derivation":      2,
    "derivation_list": 3,
    "grammar":         4,
    "name_list":       5,
    "reduction":       6,
    "reduction_block": 7,
}

goto_table = [
    [2,  6,  -1, -1, 1,  -1, 3,   5],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 8,  -1, -1, -1, -1, 3,   9],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, 10, -1, -1],
    [-1, -1, -1, -1, -1, -1, 12, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 12, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, 18, 17, -1, 16, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, 22, -1, -1, 16, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
]

reduce_symbol_sum = {
    0:  1,
    1:  1,
    2:  3,
    3:  1,
    4:  2,
    5:  1,
    6:  3,
    7:  2,
    8:  1,
    9:  1,
    10: 2,
    11: 4,
    12: 1,
    13: 2,
    14: 2,
}

reduce_to_non_terminal = {
    0:  "start",
    1:  "command_block",
    2:  "command_line",
    3:  "derivation",
    4:  "derivation",
    5:  "derivation_list",
    6:  "derivation_list",
    7:  "grammar",
    8:  "grammar",
    9:  "name_list",
    10: "name_list",
    11: "reduction",
    12: "reduction_block",
    13: "reduction_block",
    14: "command_block",
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
            if token_class in ["skip", "comment"]:
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
    command_list = []
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
            if token_type in ["command", "name", "code"]:
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
                pass
            elif operation_number == 1:
                pass
            elif operation_number == 2:
                name_list = symbol_stack.pop()
                command = symbol_stack.pop()
                command_line = [command] + name_list
                literal_command = [command_line[0][1][1:]]
                for each_name in command_line[1:]:
                    literal_command.append(each_name[1])
                command_list.append(literal_command)
            elif operation_number == 3:
                name_list = symbol_stack.pop()
                symbol_stack.append((name_list, None))
            elif operation_number == 4:
                code = symbol_stack.pop()
                name_list = symbol_stack.pop()
                symbol_stack.append((name_list, code))
            elif operation_number == 5:
                derivation = symbol_stack.pop()
                symbol_stack.append([derivation])
            elif operation_number == 6:
                derivation = symbol_stack.pop()
                derivation_list = symbol_stack.pop()
                symbol_stack.append(derivation_list + [derivation])
            elif operation_number == 7:
                pass
            elif operation_number == 8:
                pass
            elif operation_number == 9:
                name = symbol_stack.pop()
                symbol_stack.append([name])
            elif operation_number == 10:
                name = symbol_stack.pop()
                name_list = symbol_stack.pop()
                symbol_stack.append(name_list + [name])
            elif operation_number == 11:
                derivation_list = symbol_stack.pop()
                name = symbol_stack.pop()
                for derivation in derivation_list:
                    temp_derivation = [name] + derivation[0]
                    sentence = tuple([token[1] for token in temp_derivation])
                    sentence_set.add(sentence)
                    if derivation[1] is not None:
                        reduce_code[sentence] = derivation[1][1]
                    else:
                        reduce_code[sentence] = None
                pass
            elif operation_number == 12:
                pass
            elif operation_number == 13:
                pass
            elif operation_number == 14:
                pass
            else:
                raise Exception("Invalid reduce number: %d" % operation_number)
        elif operation_flag == "a":
            break
        else:
            raise Exception("Invalid action: %s" % operation)
    return sentence_set, reduce_code, command_list


def bs_grammar_analysis(filename):
    token_list, literal = bs_token_list(filename)
    sentence_set, reduce_code, command_list = bs_grammar_analyzer(token_list)
    return sentence_set, reduce_code, command_list, literal
