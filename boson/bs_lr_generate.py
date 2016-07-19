from boson.bs_analyzer_helper import bs_terminal_set, bs_non_terminal_set, bs_non_terminal_first_set, bs_non_terminal_closure, bs_mark_postfix
from boson.bs_data_package import AnalyzerTable
import boson.bs_configure as configure


def bs_lr_generate_dfa(sentence_set):
    non_terminal_set = bs_non_terminal_set(sentence_set)
    first_set = bs_non_terminal_first_set(sentence_set)
    non_terminal_closure = {}
    for non_terminal in non_terminal_set:
        non_terminal_closure[non_terminal] = bs_non_terminal_closure(non_terminal, sentence_set, non_terminal_set)
    first_flag_sentence_list = []
    for sentence in non_terminal_closure[configure.option["start_symbol"]]:
        if sentence[-1] == configure.null_symbol:
            first_flag_sentence_list.append((sentence, 2))
        else:
            first_flag_sentence_list.append((sentence, 1))
    for flag_sentence_index in range(len(first_flag_sentence_list)):
        flag_sentence = first_flag_sentence_list[flag_sentence_index]
        if flag_sentence[0][0] == configure.option["start_symbol"]:
            first_flag_sentence_list[flag_sentence_index] = ((flag_sentence[0], frozenset({configure.end_symbol})), flag_sentence[1])
    first_flag_sentence_set = bs_mark_postfix(first_flag_sentence_list, non_terminal_set, first_set)
    state_list = [frozenset(first_flag_sentence_set)]
    state_transfer = {}
    scan_index = 0
    while True:
        now_flag_sentence_set = state_list[scan_index]
        move_sentence_map = {}
        for now_flag_sentence in now_flag_sentence_set:
            now_sentence, now_index = now_flag_sentence
            if now_index < len(now_sentence[0]):
                move = now_sentence[0][now_index]
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
                move_postfix_sentence, move_index = move_flag_sentence
                if move_index < len(move_postfix_sentence[0]):
                    if move_postfix_sentence[0][move_index] in non_terminal_set:
                        temp_closure = non_terminal_closure[move_postfix_sentence[0][move_index]]
                        temp_closure_set = set()
                        for temp_sentence in temp_closure:
                            if temp_sentence[-1] == configure.null_symbol:
                                temp_closure_set.add((temp_sentence, 2))
                            else:
                                temp_closure_set.add((temp_sentence, 1))
                        new_state |= temp_closure_set
                new_state = bs_mark_postfix(list(new_state), non_terminal_set, first_set)
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


def bs_lr_generate_table(sentence_set, conflict_report=False, force=False):
    sentence_list = list(sentence_set)
    sentence_list.sort()
    for sentence_index in range(len(sentence_list)):
        if sentence_list[sentence_index][0] == configure.option["start_symbol"]:
            sentence_list[sentence_index], sentence_list[0] = sentence_list[0], sentence_list[sentence_index]
    lr_dfa_state, lr_dfa_move = bs_lr_generate_dfa(sentence_set)
    non_terminal_set = bs_non_terminal_set(sentence_set)
    terminal_set = bs_terminal_set(sentence_set, non_terminal_set)
    action_table = [[configure.boson_table_sign_error] * (len(terminal_set) + 1) for _ in range(len(lr_dfa_state))]
    goto_table = [[-1] * (len(non_terminal_set) - 1) for _ in range(len(lr_dfa_state))]
    terminal_index = {}
    non_terminal_index = {}
    reduce_symbol_sum_dict = {}
    reduce_to_non_terminal = {}
    for sentence_index in range(len(sentence_list)):
        if sentence_list[sentence_index][-1] == configure.null_symbol:
            reduce_symbol_sum_dict[sentence_index] = 0
        else:
            reduce_symbol_sum_dict[sentence_index] = len(sentence_list[sentence_index]) - 1
        reduce_to_non_terminal[sentence_index] = sentence_list[sentence_index][0]
    count = 0
    terminal_list = list(terminal_set)
    terminal_list.sort()
    for terminal in terminal_list:
        terminal_index[terminal] = count
        count += 1
    terminal_index[configure.end_symbol] = count
    count = 0
    non_terminal_list = list(non_terminal_set)
    non_terminal_list.sort()
    for non_terminal in non_terminal_list:
        non_terminal_index[non_terminal] = count
        count += 1
    for state, move_map in lr_dfa_move.items():
        for elem, next_state in move_map.items():
            if elem in terminal_set:
                action_table[state][terminal_index[elem]] = "%s%d" % (configure.boson_table_sign_shift, next_state)
            else:
                goto_table[state][non_terminal_index[elem]] = next_state
    have_conflict = False
    for state_index in range(len(lr_dfa_state)):
        state_set = lr_dfa_state[state_index]
        for state_sentence in state_set:
            sentence, flag = state_sentence
            if flag == len(sentence[0]):
                for terminal in sentence[1]:
                    reduce_number = sentence_list.index(sentence[0])
                    if action_table[state_index][terminal_index[terminal]] != configure.boson_table_sign_error:
                        if not have_conflict:
                            print()
                        have_conflict = True
                        if conflict_report:
                            old_sign = action_table[state_index][terminal_index[terminal]][0]
                            if old_sign in [configure.boson_table_sign_reduce, configure.boson_table_sign_accept]:
                                print("[Conflict state: %d] Reduce/Reduce Terminal: %s" % (state_index, terminal))
                            elif old_sign == configure.boson_table_sign_shift:
                                print("[Conflict state: %d] Shift/Reduce Terminal: %s" % (state_index, terminal))
                            else:
                                raise Exception("Invalid action: %s" %
                                                action_table[state_index][terminal_index[terminal]])
                            action_table[state_index][terminal_index[terminal]] += "/%s%d" % (configure.boson_table_sign_reduce, reduce_number)
                    else:
                        if reduce_number == 0:
                            action_table[state_index][terminal_index[terminal]] = configure.boson_table_sign_accept
                        else:
                            action_table[state_index][terminal_index[terminal]] = "%s%d" % (configure.boson_table_sign_reduce, reduce_number)
    if have_conflict and not force:
        raise Exception("This grammar is not LR !!!")
    reduce_symbol_sum = []
    reduce_to_non_terminal_index = []
    for reduce_number in range(len(reduce_symbol_sum_dict)):
        reduce_symbol_sum.append(reduce_symbol_sum_dict[reduce_number])
        reduce_to_non_terminal_index.append(non_terminal_index.get(reduce_to_non_terminal[reduce_number], 0))
    analyzer_table = AnalyzerTable()
    analyzer_table.terminal_index = terminal_index
    analyzer_table.action_table = action_table
    analyzer_table.goto_table = goto_table
    analyzer_table.reduce_symbol_sum = reduce_symbol_sum
    analyzer_table.reduce_to_non_terminal_index = reduce_to_non_terminal_index
    analyzer_table.sentence_list = sentence_list
    return analyzer_table
