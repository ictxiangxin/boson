from boson.bs_analyzer_helper import bs_terminal_set, bs_non_terminal_set
from boson.bs_slr_generate import bs_slr_generate_dfa
from boson.bs_lr_generate import bs_lr_generate_dfa
from boson.bs_data_package import AnalyzerTable
import boson.bs_configure as configure


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
        if sentence_list[sentence_index][0] == configure.option["start_symbol"]:
            sentence_list[sentence_index], sentence_list[0] = sentence_list[0], sentence_list[sentence_index]
    lalr_dfa_state, lalr_dfa_move = bs_lalr_generate_dfa(sentence_set)
    non_terminal_set = bs_non_terminal_set(sentence_set)
    terminal_set = bs_terminal_set(sentence_set, non_terminal_set)
    action_table = [[configure.boson_table_sign_error] * (len(terminal_set) + 1) for _ in range(len(lalr_dfa_state))]
    goto_table = [[-1] * (len(non_terminal_set) - 1) for _ in range(len(lalr_dfa_state))]
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
    for state, move_map in lalr_dfa_move.items():
        for elem, next_state in move_map.items():
            if elem in terminal_set:
                action_table[state][terminal_index[elem]] = "%s%d" % (configure.boson_table_sign_shift, next_state)
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
        raise Exception("This grammar is not LALR !!!")
    reduce_symbol_sum = []
    reduce_to_non_terminal_index = []
    print(reduce_to_non_terminal)
    print(non_terminal_index)
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
