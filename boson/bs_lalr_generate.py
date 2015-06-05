__author__ = 'ict'

from boson.bs_analyzer_helper import *
from boson.bs_slr_generate import bs_slr_generate_dfa
from boson.bs_lr_generate import bs_lr_generate_dfa


def bs_kernel_of_mark_state(state):
    kernel = set()
    for sentence in state:
        kernel.add((sentence[0][0], sentence[1]))
    return frozenset(kernel)


def bs_lalr_generate_dfa(sentence_set):
    sentence_postfix_mark = {}
    slr_state, slr_transfer = bs_slr_generate_dfa(sentence_set)
    lr_state, lr_transfer = bs_lr_generate_dfa(sentence_set)
    lalr_state = []
    lalr_transfer = slr_transfer
    for state in lr_state:
        state_kernel = bs_kernel_of_mark_state(state)
        state_number = slr_state.index(state_kernel)
        if state_number not in sentence_postfix_mark:
            sentence_postfix_mark[state_number] = {}
        for sentence in state:
            real_sentence = (sentence[0][0], sentence[1])
            if real_sentence not in sentence_postfix_mark[state_number]:
                sentence_postfix_mark[state_number][real_sentence] = set()
            sentence_postfix_mark[state_number][real_sentence] |= sentence[0][1]
    for state_number in range(len(slr_state)):
        temp_state = set()
        for sentence in slr_state[state_number]:
            temp_state.add(((sentence[0], frozenset(sentence_postfix_mark[state_number][sentence])), sentence[1]))
        lalr_state.append(frozenset(temp_state))
    return lalr_state, lalr_transfer


def bs_lalr_generate_table(sentence_set, conflict_report=False, force=False):
    sentence_list = list(sentence_set)
    sentence_list.sort()
    for sentence_index in range(len(sentence_list)):
        if sentence_list[sentence_index][0] == start_non_terminal_symbol:
            sentence_list[sentence_index], sentence_list[0] = sentence_list[0], sentence_list[sentence_index]
    lalr_dfa_state, lalr_dfa_move = bs_lalr_generate_dfa(sentence_set)
    non_terminal_set = bs_non_terminal_set(sentence_set)
    terminal_set = bs_terminal_set(sentence_set, non_terminal_set)
    action_table = [[boson_table_sign_error] * (len(terminal_set) + 1) for _ in range(len(lalr_dfa_state))]
    goto_table = [[-1] * (len(non_terminal_set) - 1) for _ in range(len(lalr_dfa_state))]
    terminal_index = {}
    non_terminal_index = {}
    reduce_symbol_sum = {}
    reduce_to_non_terminal = {}
    for sentence_index in range(len(sentence_list)):
        if sentence_list[sentence_index][-1] == null_symbol:
            reduce_symbol_sum[sentence_index] = 0
        else:
            reduce_symbol_sum[sentence_index] = len(sentence_list[sentence_index]) - 1
        reduce_to_non_terminal[sentence_index] = sentence_list[sentence_index][0]
    count = 0
    terminal_list = list(terminal_set)
    terminal_list.sort()
    for terminal in terminal_list:
        terminal_index[terminal] = count
        count += 1
    terminal_index[end_symbol] = count
    count = 0
    non_terminal_list = list(non_terminal_set)
    non_terminal_list.sort()
    for non_terminal in non_terminal_list:
        if non_terminal != start_non_terminal_symbol:
            non_terminal_index[non_terminal] = count
            count += 1
    for state, move_map in lalr_dfa_move.items():
        for elem, next_state in move_map.items():
            if elem in terminal_set:
                action_table[state][terminal_index[elem]] = "%s%d" % (boson_table_sign_shift, next_state)
            else:
                goto_table[state][non_terminal_index[elem]] = next_state
    have_conflict = False
    for state_index in range(len(lalr_dfa_state)):
        state_set = lalr_dfa_state[state_index]
        for state_sentence in state_set:
            sentence, flag = state_sentence
            if flag == len(sentence[0]):
                for terminal in sentence[1]:
                    reduce_number = sentence_list.index(sentence[0])
                    if action_table[state_index][terminal_index[terminal]] != boson_table_sign_error:
                        have_conflict = True
                        if conflict_report:
                            if action_table[state_index][terminal_index[terminal]][0] == boson_table_sign_reduce:
                                print("[Conflict state: %d] Reduce/Reduce Terminal: %s" % (state_index, terminal))
                            elif action_table[state_index][terminal_index[terminal]][0] == boson_table_sign_shift:
                                print("[Conflict state: %d] Shift/Reduce Terminal: %s" % (state_index, terminal))
                            else:
                                raise Exception("Invalid action: %s" %
                                                action_table[state_index][terminal_index[terminal]])
                            action_table[state_index][terminal_index[terminal]] += "/%s%d" % (boson_table_sign_reduce,
                                                                                              reduce_number)
                    else:
                        if reduce_number == 0:
                            action_table[state_index][terminal_index[terminal]] = boson_table_sign_accept
                        else:
                            action_table[state_index][terminal_index[terminal]] = "%s%d" % (boson_table_sign_reduce,
                                                                                            reduce_number)
    if have_conflict and not force:
        raise Exception("This grammar is not LALR !!!")
    return terminal_index, non_terminal_index, action_table, goto_table, reduce_symbol_sum, reduce_to_non_terminal, sentence_list
