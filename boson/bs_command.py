__author__ = 'ict'

from boson.bs_configure import *


def bs_command_true_or_false(bool_string):
    if bool_string == "true":
        return True
    elif bool_string == "false":
        return False
    else:
        raise Exception("Invalid generate_comment option: %s" % bool_string)


def bs_command_execute(command_list):
    for command in command_list:
        if command[0] == "start_symbol":
            configure["start_symbol"] = command[1]
        elif command[0] == "grammar_analyzer_name":
            configure["grammar_analyzer_name"] = command[1]
        elif command[0] == "lexical_analyzer_name":
            configure["lexical_analyzer_name"] = command[1]
        elif command[0] == "symbol_stack_name":
            configure["symbol_stack_name"] = command[1]
        elif command[0] == "generate_comment":
            configure["generate_comment"] = bs_command_true_or_false(command[1].lower())
        elif command[0] == "have_line_number":
            configure["have_line_number"] = bs_command_true_or_false(command[1].lower())
        elif command[0] == "symbol_type":
            configure["symbol_type"] = set(command[1:])
            configure["reduce_mode"] = "symbol"
        else:
            raise Exception("Invalid command: %s" % " ".join(command))