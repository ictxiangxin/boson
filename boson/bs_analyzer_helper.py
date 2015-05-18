__author__ = 'ict'

import copy

from boson.bs_configure import *


def bs_non_terminal_set(sentence_set):
    return set([sentence[0] for sentence in sentence_set])


def bs_terminal_set(sentence_set, non_terminal_set=None):
    if non_terminal_set is None:
        non_terminal_set = bs_non_terminal_set(sentence_set)
    else:
        non_terminal_set = copy.deepcopy(non_terminal_set)
    all_elem = set()
    for sentence in sentence_set:
        all_elem |= set([elem for elem in sentence])
    return all_elem - non_terminal_set


def bs_non_terminal_first_set(sentence_set):
    first_set = {}
    non_terminal_set = bs_non_terminal_set(sentence_set)
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


def bs_non_terminal_closure(non_terminal, sentence_set, non_terminal_set, visited=None):
    closure = set()
    if visited is None:
        visited = set()
    for sentence in sentence_set:
        if non_terminal == sentence[0]:
            closure.add(sentence)
            if sentence[1] in non_terminal_set and sentence[1] not in visited:
                visited.add(sentence[1])
                closure |= bs_non_terminal_closure(sentence[1], sentence_set, non_terminal_set, visited)
    return closure


def bs_mark_postfix(flag_sentence_list, non_terminal_set, first_set):
    flag_sentence_set = set()
    loop_continue = True
    while loop_continue:
        loop_continue = False
        for sentence, flag in flag_sentence_list:
            if isinstance(sentence[1], frozenset):
                real_sentence = sentence[0]
                postfix_set = sentence[1]
                if flag < len(real_sentence):
                    symbol = real_sentence[flag]
                    if symbol in non_terminal_set:
                        if flag < len(real_sentence) - 1:
                            next_symbol = real_sentence[flag + 1]
                            if next_symbol in non_terminal_set:
                                non_terminal_mark = frozenset(first_set[next_symbol])
                            else:
                                non_terminal_mark = frozenset({next_symbol})
                        else:
                            non_terminal_mark = frozenset(postfix_set)
                        for flag_sentence_index in range(len(flag_sentence_list)):
                            flag_sentence = flag_sentence_list[flag_sentence_index]
                            if flag_sentence[0][0] == symbol and not isinstance(flag_sentence[0][1], frozenset):
                                flag_sentence_list[flag_sentence_index] = \
                                    ((flag_sentence[0], non_terminal_mark), flag_sentence[1])
                                loop_continue = True
    for flag_sentence in flag_sentence_list:
        flag_sentence_set.add(((flag_sentence[0][0], frozenset(flag_sentence[0][1])), flag_sentence[1]))
    return flag_sentence_set