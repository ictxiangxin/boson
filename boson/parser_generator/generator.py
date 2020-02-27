from abc import ABCMeta
import boson.configure as configure


class ParserGenerator(metaclass=ABCMeta):
    def __init__(self, sentence_set: set):
        self._sentence_set: set = set(sentence_set)
        self._sentence_list: list = []
        self._sentence_index_mapping: dict = {}
        self._non_terminal_set: set = set()
        self._terminal_set: set = set()
        self._non_terminal_index_mapping: dict = {}
        self._terminal_index_mapping: dict = {}
        self._reduce_symbol_count: list = []
        self._reduce_non_terminal_index: list = []
        self._non_terminal_sentence_index_mapping: dict = {}
        self._first_set_mapping: dict = {}
        self._follow_set_mapping: dict = {}
        self._sentence_index_grammar_tuple_mapping: dict = {}
        self._none_grammar_tuple_sentence_index_set: set = set()
        self._reduce_number_grammar_name_mapping: dict = {}
        self._naive_reduce_number_set: set = set()
        self._augmented_sentence = (configure.boson_augmented_start, configure.boson_option['start_symbol'])

    def __augment_grammar(self):
        self._sentence_set.add(self._augmented_sentence)

    def __normalize_sentence(self):
        self._sentence_list = [self._augmented_sentence] + list(self._sentence_set - {self._augmented_sentence})
        self._sentence_index_mapping = {}
        self._reduce_symbol_count = []
        self._reduce_non_terminal_index = []
        for index, sentence in enumerate(self._sentence_list):
            if sentence[-1] == configure.boson_null_symbol:
                self._reduce_symbol_count.append(0)
            else:
                self._reduce_symbol_count.append(len(sentence) - 1)
            self._sentence_index_mapping[sentence] = index
            non_terminal = sentence[0]
            self._reduce_non_terminal_index.append(self._non_terminal_index_mapping[non_terminal])
            self._non_terminal_sentence_index_mapping.setdefault(non_terminal, set())
            self._non_terminal_sentence_index_mapping[non_terminal].add(index)

    def __generate_symbol_set(self):
        self._non_terminal_set = {sentence[0] for sentence in self._sentence_set}
        self._non_terminal_index_mapping = {}
        index_number = 0
        for symbol in self._non_terminal_set:
            self._non_terminal_index_mapping[symbol] = index_number
            index_number += 1
        right_symbol_set = set()
        for sentence in self._sentence_set:
            right_symbol_set |= set(sentence)
        self._terminal_set = right_symbol_set - self._non_terminal_set - {configure.boson_null_symbol} | {configure.boson_end_symbol}
        self._terminal_index_mapping = {}
        index_number = 0
        for symbol in self._terminal_set:
            self._terminal_index_mapping[symbol] = index_number
            index_number += 1

    def _sentence_first_set(self, sentence: tuple) -> set:
        sentence_first_set = set()
        for symbol in sentence:
            if symbol in self._non_terminal_set:
                symbol_first_set = self._first_set_mapping.get(symbol, set())
                sentence_first_set |= symbol_first_set - {configure.boson_null_symbol}
                if configure.boson_null_symbol not in symbol_first_set:
                    break
            else:
                sentence_first_set.add(symbol)
                break
        else:
            sentence_first_set.add(configure.boson_null_symbol)
        return sentence_first_set

    def _generate_non_terminal_first_set(self):
        self._first_set_mapping = {}
        old_set_size = {}
        continue_loop = True
        while continue_loop:
            continue_loop = False
            for sentence in self._sentence_set:
                self._first_set_mapping.setdefault(sentence[0], set())
                self._first_set_mapping[sentence[0]] |= self._sentence_first_set(sentence[1:])
            for non_terminal in self._non_terminal_set:
                if len(self._first_set_mapping[non_terminal]) != old_set_size.get(non_terminal, 0):
                    old_set_size[non_terminal] = len(self._first_set_mapping[non_terminal])
                    continue_loop = True

    def _generate_non_terminal_follow_set(self):
        self._follow_set_mapping = {configure.boson_augmented_start: {configure.boson_end_symbol}}
        old_set_size = {}
        continue_loop = True
        while continue_loop:
            continue_loop = False
            for sentence in self._sentence_set:
                self._follow_set_mapping.setdefault(sentence[0], set())
                scan_index = 1
                while scan_index < len(sentence):
                    current_symbol = sentence[scan_index]
                    if current_symbol in self._non_terminal_set:
                        self._follow_set_mapping.setdefault(current_symbol, set())
                        follow_set = self._sentence_first_set(sentence[scan_index + 1:])
                        self._follow_set_mapping[current_symbol] |= follow_set - {configure.boson_null_symbol}
                        if configure.boson_null_symbol in follow_set:
                            self._follow_set_mapping[current_symbol] |= self._follow_set_mapping[sentence[0]]
                    scan_index += 1
            for non_terminal in self._non_terminal_set:
                if len(self._follow_set_mapping[non_terminal]) != old_set_size.get(non_terminal, 0):
                    old_set_size[non_terminal] = len(self._follow_set_mapping[non_terminal])
                    continue_loop = True

    def non_terminal_set(self):
        return self._non_terminal_set

    def terminal_set(self):
        return self._terminal_set

    def sentence_list(self) -> list:
        return self._sentence_list

    def origin_sentence_list(self) -> list:
        return self._sentence_list[1:]

    def terminal_index_mapping(self) -> dict:
        return self._terminal_index_mapping

    def reduce_symbol_count(self) -> list:
        return self._reduce_symbol_count

    def reduce_non_terminal_index(self) -> list:
        return self._reduce_non_terminal_index

    def sentence_index_grammar_tuple_mapping(self) -> dict:
        return self._sentence_index_grammar_tuple_mapping

    def none_grammar_tuple_sentence_index_set(self) -> set:
        return self._none_grammar_tuple_sentence_index_set

    def reduce_number_grammar_name_mapping(self) -> dict:
        return self._reduce_number_grammar_name_mapping

    def naive_reduce_number_set(self) -> set:
        return self._naive_reduce_number_set

    def initialize(self):
        self.__augment_grammar()
        self.__generate_symbol_set()
        self.__normalize_sentence()

    def assemble_grammar_tuple(self, sentence_grammar_tuple_mapping: dict) -> None:
        self._sentence_index_grammar_tuple_mapping = {}
        sentence_grammar_tuple_list = list(sentence_grammar_tuple_mapping.items())
        while sentence_grammar_tuple_list:
            sentence, grammar_tuple = sentence_grammar_tuple_list.pop()
            new_grammar_tuple = []
            for grammar_node in grammar_tuple:
                if isinstance(grammar_node, tuple):
                    locator = grammar_node[0]
                    sub_grammar_tuple = grammar_node[1]
                else:
                    locator = grammar_node
                    sub_grammar_tuple = None
                if locator.startswith(configure.boson_grammar_tuple_unpack):
                    index = int(locator[1:])
                    unpack = True
                else:
                    index = int(locator)
                    unpack = False
                if index >= len(sentence) - 1:
                    raise ValueError('[Parser Generator] Grammar Node Out Of Range.')
                if unpack and sentence[index + 1] not in self._non_terminal_set:
                    raise ValueError('[Parser Generator] Terminal Symbol Can Not Unpack.')
                if sub_grammar_tuple:
                    hidden_name = sentence[index + 1]
                    if sub_grammar_tuple[0] == configure.boson_grammar_tuple_unpack:
                        sub_grammar_tuple = sub_grammar_tuple[1:]
                        unpack_node = True
                    else:
                        unpack_node = False
                    if hidden_name.startswith(configure.boson_operator_name_prefix):
                        for sentence_index in self._non_terminal_sentence_index_mapping[hidden_name]:
                            sub_sentence = self._sentence_list[sentence_index]
                            final_name = sub_sentence[-1]
                            if final_name.startswith(configure.boson_hidden_name_prefix):
                                if unpack_node:
                                    origin_tuple = sentence_grammar_tuple_mapping.get(sub_sentence, ('0',))
                                    origin_tuple = origin_tuple[:-1] + ('{}{}'.format(configure.boson_grammar_tuple_unpack, origin_tuple[-1]),)
                                    sentence_grammar_tuple_list.insert(0, (sub_sentence, origin_tuple))
                                for final_sentence_index in self._non_terminal_sentence_index_mapping[final_name]:
                                    sentence_grammar_tuple_list.append((self._sentence_list[final_sentence_index], sub_grammar_tuple))
                                if not unpack_node:
                                    break
                        else:
                            if not unpack_node:
                                raise ValueError('[Parser Generator] Symbol Closure Can Not Use Grammar Tuple.')
                    elif hidden_name.startswith(configure.boson_hidden_name_prefix):
                        for sentence_index in self._non_terminal_sentence_index_mapping[hidden_name]:
                            sentence_grammar_tuple_list.append((self._sentence_list[sentence_index], sub_grammar_tuple))
                    else:
                        raise ValueError('[Parser Generator] Symbol Can Not Use Grammar Tuple.')
                new_grammar_tuple.append((configure.boson_grammar_tuple_unpack if unpack else '') + str(index))
            self._sentence_index_grammar_tuple_mapping[self._sentence_index_mapping[sentence]] = tuple(new_grammar_tuple)
        self._none_grammar_tuple_sentence_index_set = set(range(len(self._sentence_list))) - set(self._sentence_index_grammar_tuple_mapping)

    def assemble_sentence_grammar_name(self, sentence_grammar_name_mapping: dict) -> None:
        self._reduce_number_grammar_name_mapping = {}
        for sentence, grammar_name in sentence_grammar_name_mapping.items():
            self._reduce_number_grammar_name_mapping[self._sentence_index_mapping[sentence]] = grammar_name

    def assemble_naive_sentence(self, naive_sentence_set: set) -> None:
        self._naive_reduce_number_set = set()
        for sentence in naive_sentence_set:
            self._naive_reduce_number_set.add(self._sentence_index_mapping[sentence])
