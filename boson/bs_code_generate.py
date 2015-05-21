__author__ = 'ict'

import sys

from boson.bs_code_generator_helper import *


def bs_generate_shift_code(output, mode, indent=0):
    if mode == "default":
        bs_code_output(output, "boson_stack.append(token)\n", indent)
    elif mode == "blank":
        bs_code_output(output, "\"\"\"\n", indent)
        bs_code_output(output, "Add some code for shift action here...\n", indent)
        bs_code_output(output, "\"\"\"\n", indent)
    else:
        raise Exception("Invalid shift code mode: %s" % mode)


def bs_generate_reduce_code(output, code, reduce_number, reduce_non_terminal, indent=0):
    bs_code_output(output, "boson_sentence = []\n", indent)
    bs_code_output(output, "for boson_i in range(%d):\n" % reduce_number, indent)
    bs_code_output(output, "boson_sentence.insert(0, boson_stack.pop())\n", indent + 1)
    code = code[code.index("{") + 1: code.index("}")]
    if "\r\n" in code:
        code_list = code.split("\r\n")
    else:
        code_list = code.split("\n")
    for line in code_list:
        while line[0] in [" ", "\t"]:
            line = line[1:]
        while line[-1] in [" ", "\t"]:
            line = line[: -1]
        if "$$" in line:
            line = line.replace("$$", "boson_reduce")
        else:
            bs_code_output(output, "boson_reduce = (\"non-terminal\", \"%s\")\n" % reduce_non_terminal)
        for r in range(reduce_number):
            line = line.replace("$%d" % (r + 1), "boson_sentence[%d]" % r)
        bs_code_output(output, line + "\n", indent)
    bs_code_output(output, "boson_stack.append(boson_reduce)\n", indent)


def bs_generate_lexical_analyzer(output, lex, indent=0):
    token_tuple = lex.get_token_tuple()
    ignore = lex.get_ignore()
    error = lex.get_error()
    max_token_name_len = 0
    for token in token_tuple:
        if len(token[0]) > max_token_name_len:
            max_token_name_len = len(token[0])
    bs_code_output(output, "boson_token_tuple = {\n", indent)
    for token in token_tuple:
        bs_code_output(output, "(\"%s\", " % token[0] + " " * (max_token_name_len - len(token[0])) +
                       "r\"%s\"),\n" % token[1], indent + 1)
    bs_code_output(output, "}\n", indent)
    bs_code_output(output, "\n", indent)
    bs_code_output(output, "boson_ignore = {\n", indent)
    for each_ignore in ignore:
        bs_code_output(output, "\"%s\",\n" % each_ignore, indent + 1)
    bs_code_output(output, "}\n", indent)
    bs_code_output(output, "\n", indent)
    bs_code_output(output, "boson_error = {\n", indent)
    for each_error in error:
        bs_code_output(output, "\"%s\",\n" % each_error, indent + 1)
    bs_code_output(output, "}\n", indent)
    bs_code_output(output, "\n", indent)
    bs_code_output(output, "boson_token_regular_expression = ", indent)
    bs_code_output(output, "\"|\".join(\"(?P<%s>%s)\" % pair for pair in boson_token_tuple", indent)
    bs_code_output(output, "\n", indent)


def bs_generate_python_code(analyzer_table, reduce_code, literal, lex=None, output=sys.stdout):
    terminal_index, non_terminal_index, action_table, goto_table, reduce_symbol_sum, reduce_to_non_terminal, sentence_list = \
        analyzer_table
    terminal_index_reverse_map = {}
    non_terminal_index_reverse_map = {}
    max_terminal_len = 0
    max_non_terminal_len = 0
    max_action_len = 0
    max_end_action_len = 0
    max_goto_len = 0
    max_end_goto_len = 0
    max_reduce_number_len = len(str(len(sentence_list)))
    max_literal_len = 0
    literal_map = literal[0]
    literal_reverse_map = literal[1]
    have_literal = len(literal_map) != 0
    for terminal, index in terminal_index.items():
        terminal_index_reverse_map[index] = terminal
        if len(terminal) > max_terminal_len:
            max_terminal_len = len(terminal)
    for non_terminal, index in non_terminal_index.items():
        non_terminal_index_reverse_map[index] = non_terminal
        if len(non_terminal) > max_non_terminal_len:
            max_non_terminal_len = len(non_terminal)
    for action_list in action_table:
        for action_index in range(len(action_list)):
            action = action_list[action_index]
            if len(action) > max_action_len:
                max_action_len = len(action)
            if action_index == len(action_list) - 1:
                if len(action) > max_end_action_len:
                    max_end_action_len = len(action)
    for goto_list in goto_table:
        for goto_index in range(len(goto_list)):
            goto_action = goto_list[goto_index]
            if len(str(goto_action)) > max_goto_len:
                max_goto_len = len(str(goto_action))
            if goto_index == len(goto_list) - 1:
                if len(str(goto_action)) > max_end_goto_len:
                    max_end_goto_len = len(str(goto_action))
    for literal_token in literal_map:
        if len(literal_token) > max_literal_len:
            max_literal_len = len(literal_token)
    bs_code_output(output, "\"\"\"\n")
    bs_code_output(output, boson_title + "\n", 1)
    bs_code_output(output, "By: " + boson_author + "\n", 1)
    bs_code_output(output, "Email: " + boson_author_email + "\n", 1)
    bs_code_output(output, "\n")
    bs_code_output(output, "This code generated by boson python code generator.\n", 1)
    bs_code_output(output, "\"\"\"\n")
    bs_code_output(output, "\n")
    bs_code_output(output, "\n")
    if lex is not None:
        bs_generate_lexical_analyzer(output, lex)
        bs_code_output(output, "\n")
    bs_code_output(output, "terminal_index = {\n")
    for index in range(len(terminal_index_reverse_map)):
        terminal = terminal_index_reverse_map[index]
        bs_code_output(output, "\"%s\": " % terminal + " " * (max_terminal_len - len(terminal)) + "%d,\n" % index, 1)
    bs_code_output(output, "}\n")
    bs_code_output(output, "\n")
    bs_code_output(output, "action_table = [\n")
    for action_list in action_table:
        bs_code_output(output, "[", 1)
        for action_index in range(len(action_list) - 1):
            action = action_list[action_index]
            bs_code_output(output, "\"%s\", " % action + " " * (max_action_len - len(action)))
        bs_code_output(output,  " " * (max_end_action_len - len(action_list[-1])) + "\"%s\"" % action_list[-1])
        bs_code_output(output, "],\n")
    bs_code_output(output, "]\n")
    bs_code_output(output, "\n")
    bs_code_output(output, "non_terminal_index = {\n")
    for index in range(len(non_terminal_index_reverse_map)):
        non_terminal = non_terminal_index_reverse_map[index]
        bs_code_output(output, "\"%s\": " % non_terminal + " " *
                       (max_non_terminal_len - len(non_terminal)) + "%d,\n" % index, 1)
    bs_code_output(output, "}\n")
    bs_code_output(output, "\n")
    bs_code_output(output, "goto_table = [\n")
    for goto_list in goto_table:
        bs_code_output(output, "[", 1)
        for goto_index in range(len(goto_list) - 1):
            goto_action = goto_list[goto_index]
            bs_code_output(output, "%d, " % goto_action + " " * (max_goto_len - len(str(goto_action))))
        bs_code_output(output, " " * (max_end_goto_len - len(str(goto_list[-1]))) + str(goto_list[-1]))
        bs_code_output(output, "],\n")
    bs_code_output(output, "]\n")
    bs_code_output(output, "\n")
    bs_code_output(output, "reduce_symbol_sum = {\n")
    for reduce_number, reduce_sum in reduce_symbol_sum.items():
        bs_code_output(output, "%d: " % reduce_number + " " * (max_reduce_number_len - len(str(reduce_number))) +
                       "%d,\n" % reduce_sum, 1)
    bs_code_output(output, "}\n")
    bs_code_output(output, "\n")
    bs_code_output(output, "reduce_to_non_terminal = {\n")
    for reduce_number, reduce_non_terminal in reduce_to_non_terminal.items():
        bs_code_output(output, "%d: " % reduce_number + " " * (max_reduce_number_len - len(str(reduce_number))) +
                       "\"%s\",\n" % reduce_non_terminal, 1)
    bs_code_output(output, "}\n")
    bs_code_output(output, "\n")
    if have_literal:
        bs_code_output(output, "literal_map = {\n")
        for literal_token, literal_class in literal_map.items():
            bs_code_output(output, "\"%s\": " % literal_token + " " * (max_literal_len - len(literal_token)) +
                           "\"%s\",\n" % literal_class, 1)
        bs_code_output(output, "}\n")
        bs_code_output(output, "\n")
    bs_code_output(output, "\n")
    if lex is not None:
        bs_code_output(output, "def boson_lexical_analysis(text):\n")
        bs_code_output(output, "boson_token_list = []\n", 1)
        bs_code_output(output, "for one_token in re.finditer(boson_token_regular_expression, text):\n", 1)
        bs_code_output(output, "token_class = one_token.lastgroup\n", 1)
        bs_code_output(output, "token_string = one_token.group(token_class)\n", 1)
        bs_code_output(output, "if token_class in boson_ignore:\n", 1)
        bs_code_output(output, "continue\n", 2)
        bs_code_output(output, "if token_class in boson_error:\n", 1)
        bs_code_output(output, "raise Exception(\"Invalid token: (%s, \"%s\")\" % (token_class, token_string))\n", 2)
        bs_code_output(output, "boson_token_list.append((token_class, token_string))\n", 1)
        bs_code_output(output, "boson_token_list.append((\"%s\", \"\"))\n" % end_symbol, 1)
        bs_code_output(output, "return boson_token_list\n", 1)
        bs_code_output(output, "\n")
        bs_code_output(output, "\n")
    bs_code_output(output, "def boson_grammar_analysis(token_list):\n")
    bs_code_output(output, "\"\"\"\n", 1)
    bs_code_output(output, "Add some data structure definition code here...\n", 2)
    bs_code_output(output, "\"\"\"\n", 1)
    bs_code_output(output, "boson_stack = []\n", 1)
    bs_code_output(output, "stack = [0]\n", 1)
    bs_code_output(output, "token_index = 0\n", 1)
    bs_code_output(output, "while token_index < len(token_list):\n", 1)
    bs_code_output(output, "token = token_list[token_index]\n", 2)
    if have_literal:
        bs_code_output(output, "if token[1] in literal_map:\n", 2)
        bs_code_output(output, "token_type = literal_map[token[1]]\n", 3)
        bs_code_output(output, "else:\n", 2)
        bs_code_output(output, "token_type = token[0]\n", 3)
    else:
        bs_code_output(output, "token_type = token[0]\n", 2)
    bs_code_output(output, "now_state = stack[-1]\n", 2)
    bs_code_output(output, "operation = action_table[now_state][terminal_index[token_type]]\n", 2)
    bs_code_output(output, "operation_flag = operation[0]\n", 2)
    bs_code_output(output, "if operation_flag == \"e\":\n", 2)
    bs_code_output(output, "raise Exception(\"Grammar error: \" + \" \".join([t[1] for t in token_list]))\n", 3)
    bs_code_output(output, "elif operation_flag == \"s\":\n", 2)
    bs_code_output(output, "operation_number = int(operation[1:])\n", 3)
    bs_code_output(output, "stack.append(operation_number)\n", 3)
    bs_code_output(output, "token_index += 1\n", 3)
    bs_generate_shift_code(output, "default", 3)
    bs_code_output(output, "elif operation_flag == \"r\":\n", 2)
    bs_code_output(output, "operation_number = int(operation[1:])\n", 3)
    bs_code_output(output, "reduce_sum = reduce_symbol_sum[operation_number]\n", 3)
    bs_code_output(output, "for _ in range(reduce_sum):\n", 3)
    bs_code_output(output, "stack.pop()\n", 4)
    bs_code_output(output, "now_state = stack[-1]\n", 3)
    bs_code_output(output, "now_non_terminal_index = non_terminal_index[reduce_to_non_terminal[operation_number]]\n", 3)
    bs_code_output(output, "stack.append(goto_table[now_state][now_non_terminal_index])\n", 3)
    for reduce_index in range(1, len(sentence_list)):
        if reduce_index == 1:
            bs_code_output(output, "if operation_number == 1:\n", 3)
        else:
            bs_code_output(output, "elif operation_number == %d:\n" % reduce_index, 3)
        literal_sentence = list(sentence_list[reduce_index])
        if have_literal:
            for now_sentence_index in range(len(literal_sentence)):
                if literal_sentence[now_sentence_index] in literal_reverse_map:
                    literal_sentence[now_sentence_index] =\
                        "'" + literal_reverse_map[literal_sentence[now_sentence_index]] + "'"
        bs_code_output(output, "# %s -> %s\n" % (literal_sentence[0], " ".join(literal_sentence[1:])), 4)
        if reduce_code[sentence_list[reduce_index]] is not None:
            bs_generate_reduce_code(output, reduce_code[sentence_list[reduce_index]], reduce_symbol_sum[reduce_index],
                                    reduce_to_non_terminal[reduce_index], 4)
        else:
            bs_code_output(output, "pass\n", 4)
    bs_code_output(output, "else:\n", 3)
    bs_code_output(output, "raise Exception(\"Invalid reduce number: %d\" % operation_number)\n", 4)
    bs_code_output(output, "elif operation_flag == \"a\":\n", 2)
    bs_code_output(output, "break\n", 3)
    bs_code_output(output, "else:\n", 2)
    bs_code_output(output, "raise Exception(\"Invalid action: %s\" % operation)\n", 3)
    bs_code_output(output, "\"\"\"\n", 1)
    bs_code_output(output, "Add some postprocessing code here...\n", 2)
    bs_code_output(output, "\"\"\"\n", 1)
