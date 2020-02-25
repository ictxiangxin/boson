from boson.parser_generator.bottom_up_generator import BottomUpCanonicalParserGenerator
import boson.configure as configure


class LRParserGenerator(BottomUpCanonicalParserGenerator):
    def __init__(self, sentence_set: set):
        super().__init__(sentence_set)

    def __generate_mark_postfix(self, flag_sentence_list: list) -> set:
        loop_continue = True
        while loop_continue:
            loop_continue = False
            for sentence, flag in flag_sentence_list:
                real_sentence, postfix_set = sentence
                if postfix_set is not None:
                    if flag < len(real_sentence):
                        symbol = real_sentence[flag]
                        if symbol in self._non_terminal_set:
                            non_terminal_mark = set()
                            scan_index = flag + 1
                            while scan_index < len(real_sentence):
                                target = real_sentence[scan_index]
                                if target in self._non_terminal_set:
                                    target_first_set = self._first_set_mapping[target]
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
                            for flag_sentence_index in range(len(flag_sentence_list)):
                                (sentence, mark_postfix), flag = flag_sentence_list[flag_sentence_index]
                                if sentence[0] == symbol:
                                    if mark_postfix is None:
                                        new_mark_postfix = non_terminal_mark
                                        loop_continue = True
                                    else:
                                        new_mark_postfix = set(mark_postfix) | non_terminal_mark
                                        if len(new_mark_postfix) > len(mark_postfix):
                                            loop_continue = True
                                    flag_sentence_list[flag_sentence_index] = ((sentence, frozenset(new_mark_postfix)), flag)
        return set(flag_sentence_list)

    def initialize_start_state(self):
        first_flag_sentence_list = []
        for sentence in self._non_terminal_closure[configure.boson_augmented_start]:
            flag = 2 if sentence[-1] == configure.boson_null_symbol else 1
            mark_postfix = frozenset({configure.boson_end_symbol}) if sentence[0] == configure.boson_augmented_start else None
            first_flag_sentence_list.append(((sentence, mark_postfix), flag))
        return self.__generate_mark_postfix(first_flag_sentence_list)

    def sentence_look_ahead_set(self, sentence: tuple) -> (frozenset, None):
        return None

    def state_post_processing(self, state: set) -> set:
        return self.__generate_mark_postfix(list(state))
