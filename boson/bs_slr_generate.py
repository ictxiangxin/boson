__author__ = 'ict'

from boson.bs_analyzer_helper import *


def bs_slr_generate_dfa(sentence_set):
    non_terminal_set = bs_non_terminal_set(sentence_set)
    non_terminal_closure = {}
    for non_terminal in non_terminal_set:
        non_terminal_closure[non_terminal] = bs_non_terminal_closure(non_terminal, sentence_set, non_terminal_set)
    first_flag_sentence_set = []
    for sentence in non_terminal_closure[start_non_terminal_symbol]:
        if sentence[-1] == null_symbol:
            first_flag_sentence_set.append((sentence, 2))
        else:
            first_flag_sentence_set.append((sentence, 1))
    state_list = [frozenset(first_flag_sentence_set)]
    state_transfer = {}
    scan_index = 0
    while True:
        now_flag_sentence_set = state_list[scan_index]
        move_sentence_map = {}
        for now_flag_sentence in now_flag_sentence_set:
            now_sentence, now_index = now_flag_sentence
            if now_index < len(now_sentence):
                move = now_sentence[now_index]
                if move not in move_sentence_map:
                    move_sentence_map[move] = set()
                move_sentence_map[move].add(now_flag_sentence)
        for move, move_flag_sentence_set in move_sentence_map.items():
            new_state = set()
            for move_flag_sentence in move_flag_sentence_set:
                move_flag_sentence = list(move_flag_sentence)
                move_flag_sentence[1] += 1
                move_flag_sentence = tuple(move_flag_sentence)
                new_state.add(move_flag_sentence)
                move_sentence, move_index = move_flag_sentence
                if move_index < len(move_sentence):
                    if move_sentence[move_index] in non_terminal_set:
                        temp_closure = non_terminal_closure[move_sentence[move_index]]
                        temp_closure_set = set()
                        for temp_sentence in temp_closure:
                            if temp_sentence[-1] == null_symbol:
                                temp_closure_set.add((temp_sentence, 2))
                            else:
                                temp_closure_set.add((temp_sentence, 1))
                        new_state |= temp_closure_set
            hashable_new_state = frozenset(new_state)
            if scan_index not in state_transfer:
                state_transfer[scan_index] = {}
            if hashable_new_state in state_list:
                old_index = state_list.index(hashable_new_state)
                state_transfer[scan_index][move] = old_index
            else:
                state_list.append(hashable_new_state)
                state_transfer[scan_index][move] = len(state_list) - 1
        scan_index += 1
        if scan_index >= len(state_list):
            break
    return state_list, state_transfer


def bs_slr_generate_table(sentence_set, conflict_report=False, force=False):
    sentence_list = list(sentence_set)
    sentence_list.sort()
    for sentence_index in range(len(sentence_list)):
        if sentence_list[sentence_index][0] == start_non_terminal_symbol:
            sentence_list[sentence_index], sentence_list[0] = sentence_list[0], sentence_list[sentence_index]
    slr_dfa_state, slr_dfa_move = bs_slr_generate_dfa(sentence_set)
    follow_set = bs_non_terminal_follow_set(sentence_set)
    non_terminal_set = bs_non_terminal_set(sentence_set)
    terminal_set = bs_terminal_set(sentence_set, non_terminal_set)
    action_table = [[boson_table_sign_error] * (len(terminal_set) + 1) for _ in range(len(slr_dfa_state))]
    goto_table = [[-1] * (len(non_terminal_set) - 1) for _ in range(len(slr_dfa_state))]
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
    for state, move_map in slr_dfa_move.items():
        for elem, next_state in move_map.items():
            if elem in terminal_set:
                action_table[state][terminal_index[elem]] = "%s%d" % (boson_table_sign_shift, next_state)
            else:
                goto_table[state][non_terminal_index[elem]] = next_state
    have_conflict = False
    for state_index in range(len(slr_dfa_state)):
        state_set = slr_dfa_state[state_index]
        for state_sentence in state_set:
            sentence, flag = state_sentence
            if flag == len(sentence):
                for terminal in follow_set[sentence[0]]:
                    reduce_number = sentence_list.index(sentence)
                    if action_table[state_index][terminal_index[terminal]] != boson_table_sign_error:
                        if not have_conflict:
                            print()
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
        raise Exception("This grammar is not SLR !!!")
    return terminal_index, non_terminal_index, action_table, goto_table, reduce_symbol_sum, reduce_to_non_terminal, sentence_list
