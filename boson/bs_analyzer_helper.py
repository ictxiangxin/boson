import copy
import boson.bs_configure as configure


def bs_non_terminal_set(sentence_set):
    return set([sentence[0] for sentence in sentence_set])


def bs_terminal_set(sentence_set, non_terminal_set=None):
    if non_terminal_set is None:
        non_terminal_set = bs_non_terminal_set(sentence_set)
    else:
        non_terminal_set = copy.deepcopy(non_terminal_set)
    non_terminal_set.add(configure.null_symbol)
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
            left = sentence[0]
            if left not in first_set:
                first_set[left] = set()
            scan_index = 1
            while True:
                target = sentence[scan_index]
                if target in non_terminal_set:
                    if target not in first_set:
                        first_set[target] = set()
                    else:
                        temp_first_set = copy.copy(first_set[target])
                        if configure.null_symbol in temp_first_set:
                            temp_first_set.remove(configure.null_symbol)
                        first_set[left] |= temp_first_set
                else:
                    first_set[left].add(target)
                if target in non_terminal_set and configure.null_symbol in first_set[target]:
                    scan_index += 1
                else:
                    break
                if scan_index >= len(sentence):
                    first_set[left].add(configure.null_symbol)
                    break
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
    follow_set = {configure.option["start_symbol"]: {configure.end_symbol}}
    non_terminal_set = set([sentence[0] for sentence in sentence_set])
    old_set_size = {non_terminal: 0 for non_terminal in non_terminal_set}
    continue_loop = True
    while continue_loop:
        continue_loop = False
        for sentence in sentence_set:
            left = sentence[0]
            if left in non_terminal_set and left not in follow_set:
                follow_set[left] = set()
            scan_index = 1
            while scan_index < len(sentence):
                current_symbol = sentence[scan_index]
                if current_symbol in non_terminal_set:
                    if current_symbol in non_terminal_set and current_symbol not in follow_set:
                        follow_set[current_symbol] = set()
                    if scan_index != len(sentence) - 1:
                        next_symbol_list = sentence[scan_index + 1:]
                        next_symbol_first = set()
                        sub_scan_index = 0
                        while True:
                            target = next_symbol_list[sub_scan_index]
                            if target in non_terminal_set:
                                temp_first_set = copy.copy(first_set[target])
                                if configure.null_symbol in temp_first_set:
                                    temp_first_set.remove(configure.null_symbol)
                                next_symbol_first |= temp_first_set
                            else:
                                next_symbol_first.add(target)
                            if target in non_terminal_set and configure.null_symbol in first_set[target]:
                                sub_scan_index += 1
                            else:
                                break
                            if sub_scan_index >= len(next_symbol_list):
                                next_symbol_first.add(configure.null_symbol)
                                break
                        temp_symbol_first = copy.copy(next_symbol_first)
                        if configure.null_symbol in temp_symbol_first:
                            temp_symbol_first.remove(configure.null_symbol)
                        follow_set[current_symbol] |= temp_symbol_first
                        if configure.null_symbol in next_symbol_first:
                            if left in non_terminal_set and left not in follow_set:
                                follow_set[left] = set()
                            follow_set[current_symbol] |= follow_set[left]
                    else:
                        if left in non_terminal_set and left not in follow_set:
                            follow_set[left] = set()
                        follow_set[current_symbol] |= follow_set[left]
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
                                temp_first_set = copy.copy(first_set[next_symbol])
                                if configure.null_symbol in temp_first_set:
                                    temp_first_set.remove(configure.null_symbol)
                                    temp_first_set |= postfix_set
                                non_terminal_mark = frozenset(temp_first_set)
                            else:
                                non_terminal_mark = frozenset({next_symbol})
                        else:
                            non_terminal_mark = frozenset(postfix_set)
                        for flag_sentence_index in range(len(flag_sentence_list)):
                            flag_sentence = flag_sentence_list[flag_sentence_index]
                            if isinstance(flag_sentence[0][1], frozenset):
                                if flag_sentence[0][0][0] == symbol:
                                    old_mark_sum = len(flag_sentence_list[flag_sentence_index][0][1])
                                    temp_mark_set = set(flag_sentence_list[flag_sentence_index][0][1])
                                    temp_mark_set |= non_terminal_mark
                                    flag_sentence_list[flag_sentence_index] = \
                                        ((flag_sentence[0][0], frozenset(temp_mark_set)), flag_sentence[1])
                                    if len(flag_sentence_list[flag_sentence_index][0][1]) > old_mark_sum:
                                        loop_continue = True
                            else:
                                if flag_sentence[0][0] == symbol:
                                    flag_sentence_list[flag_sentence_index] = \
                                        ((flag_sentence[0], non_terminal_mark), flag_sentence[1])
                                    loop_continue = True
    for flag_sentence in flag_sentence_list:
        flag_sentence_set.add(((flag_sentence[0][0], frozenset(flag_sentence[0][1])), flag_sentence[1]))
    return flag_sentence_set
