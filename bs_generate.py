__author__ = 'ict'

import copy

from bs_grammmar_normal_form import start_non_terminal_symbol, end_symbol


def bs_non_terminal_closure(non_terminal, sentense_set, non_terminal_set, visited=None):
    closure = set()
    if visited is None:
        visited = set()
    for sentense in sentense_set:
        if non_terminal == sentense[0]:
            closure.add(sentense)
            if sentense[1] in non_terminal_set and sentense[1] not in visited:
                visited.add(sentense[1])
                closure |= bs_non_terminal_closure(sentense[1], sentense_set, non_terminal_set, visited)
    return closure


def bs_move_set(state_sentence_set):
    move_set = set()
    for state_sentence in state_sentence_set:
        sentence, index = state_sentence
        if index < len(sentence):
            move_set.add(sentence[index])
    return move_set


def bs_generate_slr_dfa(sentense_set):
    non_terminal_set = set()
    non_terminal_closure = {}
    first_flag_sentence_set = []
    for sentence in sentense_set:
        non_terminal_set.add(sentence[0])
        first_flag_sentence_set.append((sentence, 1))
    first_flag_sentence_set = tuple(first_flag_sentence_set)
    for non_terminal in non_terminal_set:
        non_terminal_closure[non_terminal] = bs_non_terminal_closure(non_terminal, sentense_set, non_terminal_set)
    state_list = [frozenset(first_flag_sentence_set)]
    state_transfer = {}
    scan_index = 0
    while True:
        now_flag_sentence_set = state_list[scan_index]
        move_set = bs_move_set(now_flag_sentence_set)
        move_sentence_map = {}
        for now_flag_sentence in now_flag_sentence_set:
            now_sentence, now_index = now_flag_sentence
            if now_index < len(now_sentence):
                if now_sentence[now_index] in move_set:
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


def bs_non_terminal_first_set(sentence_set):
    first_set = {}
    non_terminal_set = set([sentence[0] for sentence in sentence_set])
    old_set_size = {non_terminal: 0 for non_terminal in non_terminal_set}
    continue_loop = True
    while continue_loop:
        continue_loop = False
        for sentence in sentence_set:
            if sentence[0] not in first_set:
                first_set[sentence[0]] = set()
            if sentence[1] in non_terminal_set:
                if sentence[1] not in first_set:
                    first_set[sentence[1]] = set()
                else:
                    first_set[sentence[0]] |= first_set[sentence[1]]
            else:
                first_set[sentence[0]].add(sentence[1])
        for non_terminal in non_terminal_set:
            print(non_terminal)
            print(first_set[non_terminal])
            if len(first_set[non_terminal]) != old_set_size[non_terminal]:
                old_set_size[non_terminal] = len(first_set[non_terminal])
                continue_loop = True
    return first_set


def bs_non_terminal_follow_set(sentence_set, first_set=None):
    if first_set is None:
        first_set = bs_non_terminal_first_set(sentence_set)
    else:
        first_set = copy.deepcopy(first_set)
    follow_set = {start_non_terminal_symbol: {end_symbol}}
    non_terminal_set = set([sentence[0] for sentence in sentence_set])
    old_set_size = {non_terminal: 0 for non_terminal in non_terminal_set}
    continue_loop = True
    while continue_loop:
        continue_loop = False
        for sentence in sentence_set:
            if sentence[0] in non_terminal_set and sentence[0] not in follow_set:
                follow_set[sentence[0]] = set()
            scan_index = 1
            while scan_index < len(sentence):
                if sentence[scan_index] in non_terminal_set:
                    if sentence[scan_index] in non_terminal_set and sentence[scan_index] not in follow_set:
                        follow_set[sentence[scan_index]] = set()
                    if scan_index != len(sentence) - 1:
                        next_symbol = sentence[scan_index + 1]
                        if next_symbol in non_terminal_set:
                            if next_symbol in non_terminal_set and next_symbol not in follow_set:
                                follow_set[next_symbol] = set()
                            else:
                                follow_set[sentence[scan_index]] |= first_set[next_symbol]
                        else:
                            follow_set[sentence[scan_index]].add(next_symbol)
                    else:
                        if sentence[0] in non_terminal_set and sentence[0] not in follow_set:
                            follow_set[sentence[0]] = set()
                        follow_set[sentence[scan_index]] |= follow_set[sentence[0]]
                scan_index += 1
        for non_terminal in non_terminal_set:
            if len(follow_set[non_terminal]) != old_set_size[non_terminal]:
                old_set_size[non_terminal] = len(follow_set[non_terminal])
                continue_loop = True
    return follow_set