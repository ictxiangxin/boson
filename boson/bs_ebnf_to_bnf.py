__author__ = 'ict'

import re
import sys

from boson.bs_configure import *


token_tuple = [
    ("name",     r"[_a-zA-Z][_a-zA-Z0-9]*"),
    ("literal",  r"\'.*?[^\\]\'|\".*?[^\\]\""),
    ("reduce",   r"="),
    ("concat",   r","),
    ("or",       r"\|"),
    ("repet_l",  r"\{"),
    ("repet_r",  r"\}"),
    ("option_l", r"\["),
    ("option_r", r"\]"),
    ("group_l",  r"\("),
    ("group_r",  r"\)"),
    ("command",  r"%[_a-zA-Z]+"),
    ("comment",  r"#[^(\r\n|\n)]*"),
    ("end",      r"\;"),
    ("skip",     r"[ \t]+"),
    ("newline",  r"\n|\r\n"),
    ("invalid",  r"."),
]

token_regular_expression = "|".join("(?P<%s>%s)" % pair for pair in token_tuple)

terminal_index = {
    "concat":   0,
    "end":      1,
    "group_l":  2,
    "group_r":  3,
    "literal":  4,
    "name":     5,
    "option_l": 6,
    "option_r": 7,
    "or":       8,
    "reduce":   9,
    "repet_l":  10,
    "repet_r":  11,
    "$":        12,
}

action_table = [
    ["e",   "e",   "e",   "e",   "e",   "s2",  "e",   "e",   "e",   "e",   "e",   "e",    "e"],
    ["e",   "e",   "e",   "e",   "e",   "s2",  "e",   "e",   "e",   "e",   "e",   "e",    "a"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "s5",  "e",   "e",    "e"],
    ["e",   "e",   "e",   "e",   "e",   "r1",  "e",   "e",   "e",   "e",   "e",   "e",   "r1"],
    ["e",   "e",   "e",   "e",   "e",   "r2",  "e",   "e",   "e",   "e",   "e",   "e",   "r2"],
    ["e",   "e",   "s12", "e",   "s6",  "s14", "s8",  "e",   "e",   "e",   "s13", "e",    "e"],
    ["r3",  "r3",  "e",   "r3",  "e",   "e",   "e",   "r3",  "r3",  "e",   "e",   "r3",   "e"],
    ["r5",  "r5",  "e",   "r5",  "e",   "e",   "e",   "r5",  "r5",  "e",   "e",   "r5",   "e"],
    ["e",   "e",   "s12", "e",   "s6",  "s14", "s8",  "e",   "e",   "e",   "s13", "e",    "e"],
    ["r10", "r10", "e",   "r10", "e",   "e",   "e",   "r10", "r10", "e",   "e",   "r10",  "e"],
    ["e",   "s17", "e",   "e",   "e",   "e",   "e",   "e",   "s16", "e",   "e",   "e",    "e"],
    ["s18", "r12", "e",   "r12", "e",   "e",   "e",   "r12", "r12", "e",   "e",   "r12",  "e"],
    ["e",   "e",   "s12", "e",   "s6",  "s14", "s8",  "e",   "e",   "e",   "s13", "e",    "e"],
    ["e",   "e",   "s12", "e",   "s6",  "s14", "s8",  "e",   "e",   "e",   "s13", "e",    "e"],
    ["r4",  "r4",  "e",   "r4",  "e",   "e",   "e",   "r4",  "r4",  "e",   "e",   "r4",   "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "e",   "s21", "s16", "e",   "e",   "e",    "e"],
    ["e",   "e",   "s12", "e",   "s6",  "s14", "s8",  "e",   "e",   "e",   "s13", "e",    "e"],
    ["e",   "e",   "e",   "e",   "e",   "r9",  "e",   "e",   "e",   "e",   "e",   "e",   "r9"],
    ["e",   "e",   "s12", "e",   "s6",  "s14", "s8",  "e",   "e",   "e",   "s13", "e",    "e"],
    ["e",   "e",   "e",   "s24", "e",   "e",   "e",   "e",   "s16", "e",   "e",   "e",    "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "s16", "e",   "e",   "s25",  "e"],
    ["r7",  "r7",  "e",   "r7",  "e",   "e",   "e",   "r7",  "r7",  "e",   "e",   "r7",   "e"],
    ["s18", "r13", "e",   "r13", "e",   "e",   "e",   "r13", "r13", "e",   "e",   "r13",  "e"],
    ["r11", "r11", "e",   "r11", "e",   "e",   "e",   "r11", "r11", "e",   "e",   "r11",  "e"],
    ["r6",  "r6",  "e",   "r6",  "e",   "e",   "e",   "r6",  "r6",  "e",   "e",   "r6",   "e"],
    ["r8",  "r8",  "e",   "r8",  "e",   "e",   "e",   "r8",  "r8",  "e",   "e",   "r8",   "e"],
]

non_terminal_index = {
    "ebnf":           0,
    "ebnf_list":      1,
    "element":        2,
    "item":           3,
    "statement":      4,
    "statement_list": 5,
}

goto_table = [
    [3,  1,  -1, -1, -1, -1],
    [4,  -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, 7,  9,  11, 10],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, 7,  9,  11, 15],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, 7,  9,  11, 19],
    [-1, -1, 7,  9,  11, 20],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, 7,  9,  22, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, 7,  23, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
]

reduce_symbol_sum = {
    0:  1,
    1:  1,
    2:  2,
    3:  1,
    4:  1,
    5:  1,
    6:  3,
    7:  3,
    8:  3,
    9:  4,
    10: 1,
    11: 3,
    12: 1,
    13: 3,
}

reduce_to_non_terminal = {
    0:  "start",
    1:  "ebnf_list",
    2:  "ebnf_list",
    3:  "element",
    4:  "element",
    5:  "item",
    6:  "item",
    7:  "item",
    8:  "item",
    9:  "ebnf",
    10: "statement",
    11: "statement",
    12: "statement_list",
    13: "statement_list",
}


def bs_ebnf_token_list(filename):
    with open(filename, "r") as fp:
        text = fp.read()
        token_list = list()
        line_number = 1
        for one_token in re.finditer(token_regular_expression, text):
            token_class = one_token.lastgroup
            token_string = one_token.group(token_class)
            if token_class in ["skip", "comment"]:
                pass
            elif token_class == "newline":
                line_number += 1
            elif token_class == "invalid":
                raise RuntimeError("[Line: %d] Invalid token: %s" % (line_number, token_string))
            else:
                token_list.append((token_class, token_string))
    token_list.append((end_symbol, ""))
    return token_list


def bs_ebnf_grammar_analyzer(token_list):
    ast_list = []
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
            print(token)
            raise Exception("Grammar error: " + " ".join([t[1] for t in token_list]))
        elif operation_flag == "s":
            operation_number = int(operation[1:])
            stack.append(operation_number)
            token_index += 1
            if token_type in ["name", "literal"]:
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
                pass
            elif operation_number == 3:
                pass
            elif operation_number == 4:
                pass
            elif operation_number == 5:
                pass
            elif operation_number == 6:
                statement = symbol_stack.pop()
                symbol_stack.append(["<group>", statement])
            elif operation_number == 7:
                statement = symbol_stack.pop()
                symbol_stack.append(["<option>", statement])
            elif operation_number == 8:
                statement = symbol_stack.pop()
                symbol_stack.append(["<repet>", statement])
            elif operation_number == 9:
                statement_list = symbol_stack.pop()
                name = symbol_stack.pop()
                ast_list.append((name, statement_list))
            elif operation_number == 10:
                item = symbol_stack.pop()
                symbol_stack.append([item])
            elif operation_number == 11:
                item = symbol_stack.pop()
                statement = symbol_stack.pop()
                symbol_stack.append(statement + [item])
            elif operation_number == 12:
                statement = symbol_stack.pop()
                symbol_stack.append([statement])
            elif operation_number == 13:
                statement = symbol_stack.pop()
                statement_list = symbol_stack.pop()
                symbol_stack.append(statement_list + [statement])
            else:
                raise Exception("Invalid reduce number: %d" % operation_number)
        elif operation_flag == "a":
            return ast_list
        else:
            raise Exception("Invalid action: %s" % operation)


def bs_convert_to_bnf(ast_list):
    setence_list = []
    non_terminal_sub = {}
    for ast in ast_list:
        left = ast[0]
        non_terminal_sub[left] = 0
        production_list = ast[1]
        for production in production_list:
            setence_list.append([left] + production)
    new_sentence_list = setence_list
    continue_loop = True
    while continue_loop:
        continue_loop = False
        setence_list = new_sentence_list
        new_sentence_list = []
        for sentence in setence_list:
            left = sentence[0]
            is_special = False
            for index in range(1, len(sentence)):
                if isinstance(sentence[index], list):
                    is_special = True
                    if sentence[index][0][0] == "<" and sentence[index][0][-1] == ">":
                        sub_sentence = sentence[index][1]
                        ebnf_type = sentence[index][0][1: -1]
                        if len(sub_sentence) == 1:
                            symbol = sub_sentence[0]
                        else:
                            symbol = left + "_%d" % non_terminal_sub[left]
                            non_terminal_sub[left] += 1
                            new_sentence_list.append([symbol] + sub_sentence)
                        if ebnf_type == "repet":
                            replace_symbol = left + "_%d" % non_terminal_sub[left]
                            non_terminal_sub[left] += 1
                            sentence[index] = replace_symbol
                            new_sentence_list.append([replace_symbol, replace_symbol, symbol])
                            new_sentence_list.append([replace_symbol, null_symbol])
                        elif ebnf_type == "option":
                            sentence[index] = symbol
                            new_sentence_list.append([symbol, null_symbol])
                        elif ebnf_type == "group":
                            sentence[index] = symbol
                        new_sentence_list.append(sentence)
                    else:
                        new_sentence_list.append([left] + sentence[index])
            if not is_special:
                new_sentence_list.append(sentence)
            else:
                continue_loop = True
    production_dict = {}
    for sentence in new_sentence_list:
        left = sentence[0]
        if left not in production_dict:
            production_dict[left] = set()
        production_dict[left].add(tuple(sentence[1:]))
    collision_dict = {}
    for non_terminal, production_set in production_dict.items():
        frozen_production = frozenset(production_set)
        if frozen_production not in collision_dict:
            collision_dict[frozen_production] = {non_terminal}
        collision_dict[frozen_production].add(non_terminal)
    production_dict = {}
    name_map = {}
    for production_set, non_terminal_set in collision_dict.items():
        non_terminal_list = list(non_terminal_set)
        non_terminal_list.sort()
        non_terminal = non_terminal_list[0]
        for each_non_terminal in non_terminal_list:
            name_map[each_non_terminal] = non_terminal
        production_dict[non_terminal] = set(production_set)
    bnf_list = []
    for non_terminal, production_set in production_dict.items():
        temp_production_list = []
        for production in production_set:
            temp_list = []
            for elem in production:
                if elem in name_map:
                    temp_list.append(name_map[elem])
                else:
                    temp_list.append(elem)
            temp_production_list.append(temp_list)
        bnf_list.append([non_terminal, temp_production_list])
    return bnf_list


def bs_bnf_list(filename):
    token_list = bs_ebnf_token_list(filename)
    ast_list = bs_ebnf_grammar_analyzer(token_list)
    bnf_list = bs_convert_to_bnf(ast_list)
    return bnf_list


def bs_ebnf_to_sentence_set(filename):
    sentence_set = set()
    bnf_list = bs_bnf_list(filename)
    for bnf in bnf_list:
        left = bnf[0]
        production_list = bnf[1]
        for production in production_list:
            sentence_set.add(tuple([left] + production))
    return sentence_set


def bs_ebnf_to_bnf(filename, output=sys.stdout):
    bnf_list = bs_bnf_list(filename)
    for bnf in bnf_list:
        left = bnf[0]
        production_list = bnf[1]
        left_len = len(left)
        output.write(left + " : ")
        for production_index in range(len(production_list) - 1):
            output.write(" ".join(production_list[production_index]) + "\n" + " " * left_len + " | ")
        output.write(" ".join(production_list[-1]) + "\n" + " " * left_len + " ;")
        output.write("\n\n")
