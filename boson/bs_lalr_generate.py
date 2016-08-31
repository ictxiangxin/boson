from boson.bs_generate_helper import bs_generate_table
from boson.bs_slr_generate import bs_slr_generate_dfa
from boson.bs_lr_generate import bs_lr_generate_dfa
import boson.bs_configure as configure


def bs_kernel_of_state(state):
    kernel = set()
    for sentence in state:
        kernel.add((sentence[0][0], sentence[1]))
    return frozenset(kernel)


def bs_search_index(slr_state, state_kernel):
    for state_index in range(len(slr_state)):
        slr_state_kernel = bs_kernel_of_state(slr_state[state_index])
        if state_kernel == slr_state_kernel:
            return state_index
    return None


def bs_lalr_generate_dfa(sentence_set):
    sentence_set.add((configure.boson_augmented_start, configure.option["start_symbol"]))
    sentence_postfix_mark = {}
    slr_state, slr_transfer = bs_slr_generate_dfa(sentence_set)
    lr_state, lr_transfer = bs_lr_generate_dfa(sentence_set)
    lalr_state = []
    lalr_transfer = slr_transfer
    for state in lr_state:
        state_kernel = bs_kernel_of_state(state)
        state_number = bs_search_index(slr_state, state_kernel)
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
            real_sentence = (sentence[0][0], sentence[1])
            temp_state.add(((sentence[0][0], frozenset(sentence_postfix_mark[state_number][real_sentence])), sentence[1]))
        lalr_state.append(frozenset(temp_state))
    return lalr_state, lalr_transfer


def bs_lalr_generate_table(sentence_set):
    lr_dfa_state, lr_dfa_move = bs_lalr_generate_dfa(sentence_set)
    analyzer_table = bs_generate_table(sentence_set, lr_dfa_state, lr_dfa_move)
    return analyzer_table
