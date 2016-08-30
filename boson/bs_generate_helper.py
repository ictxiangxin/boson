from boson.bs_analyzer_helper import bs_non_terminal_set, bs_terminal_set
from boson.bs_data_package import AnalyzerTable
import boson.bs_configure as configure


def bs_normalize_sentence_list(sentence_set):
    sentence_list = list(sentence_set)
    sentence_list.sort()
    for sentence_index in range(len(sentence_list)):
        if sentence_list[sentence_index][0] == configure.option["start_symbol"]:
            sentence_list = [sentence_list[sentence_index]] + sentence_list[:sentence_index] + sentence_list[sentence_index + 1:]
            break
    return sentence_list


def bs_numbering_element(container, base=0):
    container_index = {}
    count = base
    for element in container:
        container_index[element] = count
        count += 1
    return container_index


def bs_reduce_information(sentence_list, non_terminal_index):
    reduce_symbol_sum = []
    reduce_to_non_terminal_index = []
    for sentence in sentence_list:
        if sentence[-1] == configure.null_symbol:
            reduce_symbol_sum.append(0)
        else:
            reduce_symbol_sum.append(len(sentence) - 1)
            reduce_to_non_terminal_index.append(non_terminal_index[sentence[0]])
    return reduce_symbol_sum, reduce_to_non_terminal_index


def bs_generate_action_goto_table(sentence_list, terminal_index, non_terminal_index, dfa_state, dfa_move):
    action_table = [[configure.boson_table_sign_error] * (len(terminal_index) + 1) for _ in range(len(dfa_state))]
    goto_table = [[-1] * len(non_terminal_index) for _ in range(len(dfa_state))]
    for state, move_map in dfa_move.items():
        for element, next_state in move_map.items():
            if element in terminal_index:
                action_table[state][terminal_index[element]] = "%s%d" % (configure.boson_table_sign_shift, next_state)
            else:
                goto_table[state][non_terminal_index[element]] = next_state
    conflict_list = []
    for state_index in range(len(dfa_state)):
        state_set = dfa_state[state_index]
        for state_sentence in state_set:
            sentence, flag = state_sentence
            if flag == len(sentence[0]):
                for terminal in sentence[1]:
                    reduce_number = sentence_list.index(sentence[0])
                    if action_table[state_index][terminal_index[terminal]] != configure.boson_table_sign_error:
                        old_sign = action_table[state_index][terminal_index[terminal]][0]
                        if old_sign in [configure.boson_table_sign_reduce, configure.boson_table_sign_accept]:
                            conflict_list.append((state_index, configure.boson_conflict_reduce_reduce, terminal))
                        elif old_sign == configure.boson_table_sign_shift:
                            conflict_list.append((state_index, configure.boson_conflict_shift_reduce, terminal))
                        else:
                            raise Exception("Invalid action: %s" % action_table[state_index][terminal_index[terminal]])
                        action_table[state_index][terminal_index[terminal]] += "/%s%d" % (configure.boson_table_sign_reduce, reduce_number)
                    else:
                        if reduce_number == 0:
                            action_table[state_index][terminal_index[terminal]] = configure.boson_table_sign_accept
                        else:
                            action_table[state_index][terminal_index[terminal]] = "%s%d" % (configure.boson_table_sign_reduce, reduce_number)
    return action_table, goto_table, conflict_list


def bs_generate_table(sentence_set, dfa_state, dfa_move):
    sentence_list = bs_normalize_sentence_list(sentence_set)
    non_terminal_set = bs_non_terminal_set(sentence_set)
    terminal_set = bs_terminal_set(sentence_set, non_terminal_set)
    non_terminal_index = bs_numbering_element(non_terminal_set)
    terminal_index = bs_numbering_element(terminal_set | {configure.end_symbol})
    reduce_symbol_sum, reduce_to_non_terminal_index = bs_reduce_information(sentence_list, non_terminal_index)
    action_table, goto_table, conflict_list = bs_generate_action_goto_table(sentence_list, terminal_index, non_terminal_index, dfa_state, dfa_move)
    analyzer_table = AnalyzerTable()
    analyzer_table.terminal_index = terminal_index
    analyzer_table.action_table = action_table
    analyzer_table.goto_table = goto_table
    analyzer_table.reduce_symbol_sum = reduce_symbol_sum
    analyzer_table.reduce_to_non_terminal_index = reduce_to_non_terminal_index
    analyzer_table.sentence_list = sentence_list
    analyzer_table.conflict_list = conflict_list
    return analyzer_table
