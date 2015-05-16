__author__ = 'ict'

import copy

from bs_configure import *


def bs_non_terminal_set(sentence_set):
    return set([sentense[0] for sentense in sentence_set])


def bs_terminal_set(sentence_set, non_terminal_set=None):
    if non_terminal_set is None:
        non_terminal_set = bs_non_terminal_set(sentence_set)
    else:
        non_terminal_set = copy.deepcopy(non_terminal_set)
    all_elem = set()
    for sentense in sentence_set:
        all_elem |= set([elem for elem in sentense])
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