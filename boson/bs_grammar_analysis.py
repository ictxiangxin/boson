__author__ = 'ict'

import re

from boson.bs_configure import *
from boson.bs_command import bs_command_execute

token_tuple = [
    ("name",         r"[_a-zA-Z][_a-zA-Z0-9]*"),
    ("reduce",       r"\:"),
    ("or",           r"\|"),
    ("code",         r"\{.*\}"),
    ("literal",      r"\'.*?[^\\]\'|\".*?[^\\]\""),
    ("null",         r"~"),
    ("comment",      r"#[^(\r\n|\n)]*"),
    ("command",      r"%[_a-zA-Z]+"),
    ("section_head", r"@[_a-zA-Z][_a-zA-Z0-9]*"),
    ("section_text", r"@@\n[^@]*\n@@"),
    ("end",          r"\;"),
    ("skip",         r"[ \t]+"),
    ("newline",      r"\n|\r\n"),
    ("invalid",      r"."),
]

token_regular_expression = "|".join("(?P<%s>%s)" % pair for pair in token_tuple)


terminal_index = {
    "code":         0,
    "command":      1,
    "end":          2,
    "literal":      3,
    "name":         4,
    "null":         5,
    "or":           6,
    "reduce":       7,
    "section_head": 8,
    "section_text": 9,
    "$":            10,
}

action_table = [
    ["e",   "s2",  "e",   "e",   "s3",  "e",   "e",   "e",   "s8",  "e",     "e"],
    ["e",   "r19", "e",   "e",   "r19", "e",   "e",   "e",   "r19", "e",   "r19"],
    ["e",   "e",   "e",   "s10", "s11", "e",   "e",   "e",   "e",   "e",     "e"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "e",   "s13", "e",   "e",     "e"],
    ["e",   "s2",  "e",   "e",   "s3",  "e",   "e",   "e",   "s8",  "e",     "a"],
    ["e",   "r17", "e",   "e",   "r17", "e",   "e",   "e",   "r17", "e",   "r17"],
    ["e",   "r13", "e",   "e",   "r13", "e",   "e",   "e",   "r13", "e",   "r13"],
    ["e",   "r18", "e",   "e",   "r18", "e",   "e",   "e",   "r18", "e",   "r18"],
    ["e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "e",   "s15",   "e"],
    ["r10", "e",   "r10", "r10", "r10", "e",   "r10", "e",   "e",   "e",     "e"],
    ["r8",  "e",   "r8",  "r8",  "r8",  "e",   "r8",  "e",   "e",   "e",     "e"],
    ["r9",  "e",   "r9",  "r9",  "r9",  "e",   "r9",  "e",   "e",   "e",     "e"],
    ["e",   "e",   "s16", "s10", "s11", "e",   "e",   "e",   "e",   "e",     "e"],
    ["r5",  "e",   "r5",  "s10", "s11", "s19", "r5",  "e",   "e",   "e",     "e"],
    ["e",   "r12", "e",   "e",   "r12", "e",   "e",   "e",   "r12", "e",   "r12"],
    ["e",   "r15", "e",   "e",   "r15", "e",   "e",   "e",   "r15", "e",   "r15"],
    ["e",   "r16", "e",   "e",   "r16", "e",   "e",   "e",   "r16", "e",   "r16"],
    ["r11", "e",   "r11", "r11", "r11", "e",   "r11", "e",   "e",   "e",     "e"],
    ["e",   "e",   "r6",  "e",   "e",   "e",   "r6",  "e",   "e",   "e",     "e"],
    ["r4",  "e",   "r4",  "e",   "e",   "e",   "r4",  "e",   "e",   "e",     "e"],
    ["s23", "e",   "r1",  "e",   "e",   "e",   "r1",  "e",   "e",   "e",     "e"],
    ["e",   "e",   "s24", "e",   "e",   "e",   "s25", "e",   "e",   "e",     "e"],
    ["r3",  "e",   "r3",  "s10", "s11", "e",   "r3",  "e",   "e",   "e",     "e"],
    ["e",   "e",   "r2",  "e",   "e",   "e",   "r2",  "e",   "e",   "e",     "e"],
    ["e",   "r14", "e",   "e",   "r14", "e",   "e",   "e",   "r14", "e",   "r14"],
    ["r5",  "e",   "r5",  "s10", "s11", "s19", "r5",  "e",   "e",   "e",     "e"],
    ["e",   "e",   "r7",  "e",   "e",   "e",   "r7",  "e",   "e",   "e",     "e"],
]

non_terminal_index = {
    "command_statement":   0,
    "derivation":          1,
    "derivation_body":     2,
    "derivation_list":     3,
    "element":             4,
    "element_list":        5,
    "grammar":             6,
    "reduction_statement": 7,
    "section_statement":   8,
    "statement":           9,
}

goto_table = [
    [5,  -1, -1, -1, -1, -1, 4,  7,  1,   6],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, 9,  12, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [5,  -1, -1, -1, -1, -1, -1, 7,  1,  14],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, 17, -1, -1, -1, -1, -1],
    [-1, 18, 20, 21, 9,  22, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, 17, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 26, 20, -1, 9,  22, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
]

reduce_symbol_sum = {
    0:  1,
    1:  1,
    2:  2,
    3:  1,
    4:  1,
    5:  0,
    6:  1,
    7:  3,
    8:  1,
    9:  1,
    10: 1,
    11: 2,
    12: 2,
    13: 1,
    14: 4,
    15: 2,
    16: 3,
    17: 1,
    18: 1,
    19: 1,
}

reduce_to_non_terminal = {
    0:  "start",
    1:  "derivation",
    2:  "derivation",
    3:  "derivation_body",
    4:  "derivation_body",
    5:  "derivation_body",
    6:  "derivation_list",
    7:  "derivation_list",
    8:  "element",
    9:  "element",
    10: "element_list",
    11: "element_list",
    12: "grammar",
    13: "grammar",
    14: "reduction_statement",
    15: "section_statement",
    16: "command_statement",
    17: "statement",
    18: "statement",
    19: "statement",
}


def bs_token_list(filename):
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
                token_list.append((token_class, token_string, line_number))
    token_list.append((end_symbol, "", line_number))
    return token_list


def bs_grammar_analyzer(token_list):
    sentence_set = set()
    reduce_code = {}
    command_list = []
    section = {}
    literal_map = {}
    literal_reverse_map = {}
    literal_number = 1
    line_start_record = {}
    symbol_stack = []
    stack = [0]
    token_index = 0
    while token_index < len(token_list):
        token = token_list[token_index]
        token_type = token[0]
        token_line = token[2]
        if token_line not in line_start_record:
            line_start_record[token_line] = token_index
        now_state = stack[-1]
        operation = action_table[now_state][terminal_index[token_type]]
        operation_flag = operation[0]
        if operation_flag == "e":
            error_line = token[2]
            error_code = ""
            offset = 0
            for i in range(line_start_record[error_line], len(token_list)):
                if token_list[i][2] == error_line:
                    error_code += " " + token_list[i][1]
                    if i < token_index:
                        offset += len(token_list[i][1]) + 1
            error_message_head = "\nGrammar error [line %d]:" % error_line
            error_message = error_message_head + error_code + "\n"
            error_message += " " * (len(error_message_head) + offset) + "^" * len(token[1])
            raise Exception(error_message)
        elif operation_flag == "s":
            operation_number = int(operation[1:])
            stack.append(operation_number)
            token_index += 1
            if token_type in ["command", "name", "code", "literal", "section_head", "section_text"]:
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
                derivation_body = symbol_stack.pop()
                symbol_stack.append((derivation_body, None))
            elif operation_number == 2:
                code = symbol_stack.pop()
                derivation_body = symbol_stack.pop()
                symbol_stack.append((derivation_body, code))
            elif operation_number == 3:
                pass
            elif operation_number == 4:
                symbol_stack.append([(null_symbol, null_symbol)])
            elif operation_number == 5:
                symbol_stack.append([(null_symbol, null_symbol)])
            elif operation_number == 6:
                derivation = symbol_stack.pop()
                symbol_stack.append([derivation])
            elif operation_number == 7:
                derivation = symbol_stack.pop()
                derivation_list = symbol_stack.pop()
                symbol_stack.append(derivation_list + [derivation])
            elif operation_number == 8:
                literal = symbol_stack.pop()
                literal_string = literal[1][1: -1]
                if literal_string in literal_map:
                    literal_class = literal_map[literal_string]
                else:
                    literal_class = literal_templet % literal_number
                    literal_number += 1
                    literal_map[literal_string] = literal_class
                    literal_reverse_map[literal_class] = literal_string
                symbol_stack.append((literal_class, literal_string))
            elif operation_number == 9:
                pass
            elif operation_number == 10:
                element = symbol_stack.pop()
                symbol_stack.append([element])
            elif operation_number == 11:
                element = symbol_stack.pop()
                element_list = symbol_stack.pop()
                symbol_stack.append(element_list + [element])
            elif operation_number == 12:
                pass
            elif operation_number == 13:
                # grammar -> statement
                pass
            elif operation_number == 14:
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
            elif operation_number == 15:
                section_text = symbol_stack.pop()
                section_head = symbol_stack.pop()
                section[section_head[1]] = section_text[1]
            elif operation_number == 16:
                element_list = symbol_stack.pop()
                command = symbol_stack.pop()
                command_line = [command] + element_list
                literal_command = [command_line[0][1][1:]]
                for each_name in command_line[1:]:
                    literal_command.append(each_name[1])
                command_list.append(literal_command)
            elif operation_number == 17:
                pass
            elif operation_number == 18:
                pass
            elif operation_number == 19:
                pass
            else:
                raise Exception("Invalid reduce number: %d" % operation_number)
        elif operation_flag == "a":
            break
        else:
            raise Exception("Invalid action: %s" % operation)
    data_package = {
        "sentence set":        sentence_set,
        "reduce code":         reduce_code,
        "command list":        command_list,
        "section":             section,
        "literal map":         literal_map,
        "literal reverse map": literal_reverse_map,
    }
    return data_package


def bs_grammar_analysis(filename):
    token_list = bs_token_list(filename)
    data_package = bs_grammar_analyzer(token_list)
    bs_command_execute(data_package["command list"])
    del data_package["command list"]
    return data_package
