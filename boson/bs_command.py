import boson.bs_configure as configure


def bs_command_true_or_false(bool_string):
    bool_string = bool_string.lower()
    if bool_string == "true":
        return True
    elif bool_string == "false":
        return False
    else:
        raise Exception("Invalid boolean option: %s" % bool_string)


def bs_command_execute(command_list):
    for command in command_list:
        if command[0] == "start_symbol":
            configure.option["start_symbol"] = command[1]
        elif command[0] == "analyzer_class_name":
            configure.option["analyzer_class_name"] = command[1]
        elif command[0] == "grammar_class_name":
            configure.option["grammar_class_name"] = command[1]
        else:
            raise Exception("Invalid command: %s" % " ".join(command))
