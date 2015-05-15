__author__ = 'ict'


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