from boson.bs_analyzer_helper import bs_non_terminal_set, bs_non_terminal_closure, bs_non_terminal_follow_set
from boson.bs_generate_helper import bs_generate_table
import boson.bs_configure as configure


def bs_slr_generate_dfa(sentence_set):
    sentence_set.add((configure.boson_augmented_start, configure.option["start_symbol"]))
    non_terminal_set = bs_non_terminal_set(sentence_set)
    follow_set = bs_non_terminal_follow_set(sentence_set)
    non_terminal_closure = {}
    for non_terminal in non_terminal_set:
        non_terminal_closure[non_terminal] = bs_non_terminal_closure(non_terminal, sentence_set, non_terminal_set)
    first_flag_sentence_set = []
    for sentence in non_terminal_closure[configure.boson_augmented_start]:
        if sentence[-1] == configure.null_symbol:
            first_flag_sentence_set.append(((sentence, frozenset(follow_set[sentence[0]])), 2))
        else:
            first_flag_sentence_set.append(((sentence, frozenset(follow_set[sentence[0]])), 1))
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
                                temp_closure_set.add(((temp_sentence, frozenset(follow_set[temp_sentence[0]])), 2))
                            else:
                                temp_closure_set.add(((temp_sentence, frozenset(follow_set[temp_sentence[0]])), 1))
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


def bs_slr_generate_table(sentence_set):
    slr_dfa_state, slr_dfa_move = bs_slr_generate_dfa(sentence_set)
    analyzer_table = bs_generate_table(sentence_set, slr_dfa_state, slr_dfa_move)
    return analyzer_table
