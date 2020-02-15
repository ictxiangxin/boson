import boson.bs_configure as configure


def bs_non_terminal_set(sentence_set: set) -> set:
    return {sentence[0] for sentence in sentence_set}


def bs_terminal_set(sentence_set, non_terminal_set: set = None) -> set:
    if non_terminal_set is None:
        non_terminal_set = bs_non_terminal_set(sentence_set)
    all_element = set()
    for sentence in sentence_set:
        all_element |= set(sentence)
    return all_element - non_terminal_set - {configure.boson_null_symbol}


def bs_non_terminal_first_set(sentence_set: set) -> dict:
    first_set = {}
    non_terminal_set = bs_non_terminal_set(sentence_set)
    old_set_size = {non_terminal: 0 for non_terminal in non_terminal_set}
    continue_loop = True
    while continue_loop:
        continue_loop = False
        for sentence in sentence_set:
            left = sentence[0]
            first_set.setdefault(left, set())
            left_first_set = first_set[left]
            scan_index = 1
            while True:
                target = sentence[scan_index]
                if target in non_terminal_set:
                    first_set.setdefault(target, set())
                    target_first_set = first_set[target]
                    left_first_set |= target_first_set - {configure.boson_null_symbol}
                    if configure.boson_null_symbol in target_first_set:
                        scan_index += 1
                        if scan_index == len(sentence):
                            left_first_set.add(configure.boson_null_symbol)
                            break
                    else:
                        break
                else:
                    left_first_set.add(target)
                    break
        for non_terminal in non_terminal_set:
            if len(first_set[non_terminal]) != old_set_size[non_terminal]:
                old_set_size[non_terminal] = len(first_set[non_terminal])
                continue_loop = True
    return first_set


def bs_non_terminal_follow_set(sentence_set: set, first_set: set = None) -> dict:
    if first_set is None:
        first_set = bs_non_terminal_first_set(sentence_set)
    follow_set = {configure.boson_augmented_start: {configure.boson_end_symbol}}
    non_terminal_set = bs_non_terminal_set(sentence_set)
    old_set_size = {non_terminal: 0 for non_terminal in non_terminal_set}
    continue_loop = True
    while continue_loop:
        continue_loop = False
        for sentence in sentence_set:
            left = sentence[0]
            follow_set.setdefault(left, set())
            scan_index = 1
            while scan_index < len(sentence):
                current_symbol = sentence[scan_index]
                if current_symbol in non_terminal_set:
                    follow_set.setdefault(current_symbol, set())
                    if scan_index != len(sentence) - 1:
                        next_symbol_list = sentence[scan_index + 1:]
                        next_symbol_first = set()
                        sub_scan_index = 0
                        next_symbol_null_pass = False
                        while True:
                            target = next_symbol_list[sub_scan_index]
                            if target in non_terminal_set:
                                target_first_set = first_set[target]
                                next_symbol_first |= target_first_set - {configure.boson_null_symbol}
                                if configure.boson_null_symbol in target_first_set:
                                    sub_scan_index += 1
                                    if sub_scan_index == len(next_symbol_list):
                                        next_symbol_null_pass = True
                                        break
                                else:
                                    break
                            else:
                                next_symbol_first.add(target)
                                break
                        follow_set[current_symbol] |= next_symbol_first
                        if next_symbol_null_pass:
                            follow_set[current_symbol] |= follow_set[left]
                    else:
                        follow_set[current_symbol] |= follow_set[left]
                scan_index += 1
        for non_terminal in non_terminal_set:
            if len(follow_set[non_terminal]) != old_set_size[non_terminal]:
                old_set_size[non_terminal] = len(follow_set[non_terminal])
                continue_loop = True
    return follow_set


def bs_non_terminal_closure(non_terminal: str, sentence_set: set, non_terminal_set: set) -> set:
    non_terminal_closure = set()
    visited_non_terminal_set = set()
    non_terminal_list = [non_terminal]
    while len(non_terminal_list) > 0:
        non_terminal = non_terminal_list.pop()
        visited_non_terminal_set.add(non_terminal)
        for sentence in sentence_set:
            if non_terminal == sentence[0]:
                non_terminal_closure.add(sentence)
                next_symbol = sentence[1]
                if next_symbol in non_terminal_set and next_symbol not in visited_non_terminal_set:
                    non_terminal_list.append(next_symbol)
    return non_terminal_closure


def bs_mark_postfix(flag_sentence_list: list, non_terminal_set: set, first_set: dict) -> set:
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
                        non_terminal_mark = set()
                        scan_index = flag + 1
                        while True:
                            if scan_index < len(real_sentence):
                                target = real_sentence[scan_index]
                                if target in non_terminal_set:
                                    target_first_set = first_set[target]
                                    non_terminal_mark |= target_first_set - {configure.boson_null_symbol}
                                    if configure.boson_null_symbol in target_first_set:
                                        non_terminal_mark |= postfix_set
                                        scan_index += 1
                                    else:
                                        break
                                else:
                                    non_terminal_mark |= {target}
                                    break
                            else:
                                non_terminal_mark |= postfix_set
                                break
                        for flag_sentence_index in range(len(flag_sentence_list)):
                            flag_sentence = flag_sentence_list[flag_sentence_index]
                            if isinstance(flag_sentence[0][1], frozenset):
                                if flag_sentence[0][0][0] == symbol:
                                    old_mark_sum = len(flag_sentence[0][1])
                                    temp_mark_set = set(flag_sentence[0][1])
                                    temp_mark_set |= non_terminal_mark
                                    flag_sentence_list[flag_sentence_index] = ((flag_sentence[0][0], frozenset(temp_mark_set)), flag_sentence[1])
                                    if len(temp_mark_set) > old_mark_sum:
                                        loop_continue = True
                            else:
                                if flag_sentence[0][0] == symbol:
                                    flag_sentence_list[flag_sentence_index] = ((flag_sentence[0], frozenset(non_terminal_mark)), flag_sentence[1])
                                    loop_continue = True
    for flag_sentence in flag_sentence_list:
        flag_sentence_set.add(((flag_sentence[0][0], frozenset(flag_sentence[0][1])), flag_sentence[1]))
    return flag_sentence_set
