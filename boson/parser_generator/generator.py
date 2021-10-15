from abc import ABCMeta
from typing import List, Dict, Tuple, Set

import boson.configure as configure
from boson.boson_script.sentence_attribute import SentenceAttribute
from boson.option import option as boson_option
from boson.system.logger import logger


class ParserGenerator(metaclass=ABCMeta):
    def __init__(self, sentence_set: Set[Tuple[str, ...]], sentence_attribute_mapping: Dict[Tuple[str, ...], SentenceAttribute]):
        self._sentence_set: Set[Tuple[str, ...]] = set(sentence_set)
        self._sentence_attribute_mapping: Dict[Tuple[str, ...], SentenceAttribute] = sentence_attribute_mapping
        self._index_sentence_mapping: Dict[int, Tuple[str, ...]] = {}
        self._non_terminal_set: Set[str] = set()
        self._terminal_set: Set[str] = set()
        self._non_terminal_index_mapping: Dict[str, int] = {}
        self._terminal_index_mapping: Dict[str, int] = {}
        self._reduce_symbol_count: List[int] = []
        self._reduce_non_terminal_index: List[int] = []
        self._non_terminal_sentence_index_mapping: Dict[str, Set[int]] = {}
        self._first_set_mapping: Dict[str, Set[str]] = {}
        self._follow_set_mapping: Dict[str, Set[str]] = {}
        self._sentence_index_grammar_tuple_mapping: Dict[int, Tuple[str, ...]] = {}
        self._none_grammar_tuple_sentence_index_set: Set[int] = set()
        self._reduce_number_grammar_name_mapping: Dict[int, str] = {}
        self._naive_reduce_number_set: Set[int] = set()
        self._grammar_tuple_naive_sentence_set: Set[Tuple[str, ...]] = set()
        self._augmented_sentence: Tuple[str, ...] = (configure.boson_augmented_start, boson_option['parser']['start_symbol'])

    def __augment_grammar(self) -> None:
        self._sentence_set.add(self._augmented_sentence)
        self._sentence_attribute_mapping[self._augmented_sentence] = SentenceAttribute()

    def __normalize_sentence(self) -> None:
        self._reduce_symbol_count: List[int] = []
        self._reduce_non_terminal_index: List[int] = []
        reduce_symbol_count_mapping: Dict[int, int] = {}
        reduce_non_terminal_index_mapping: Dict[int, int] = {}
        current_index: int = 1
        for sentence in self._sentence_set:
            sentence_attribute: SentenceAttribute = self._sentence_attribute_mapping[sentence]
            if sentence == self._augmented_sentence:
                sentence_attribute.sentence_index = 0
            else:
                sentence_attribute.sentence_index = current_index
                current_index += 1
            self._sentence_attribute_mapping[sentence] = sentence_attribute
            if sentence[-1] == configure.boson_null_symbol:
                reduce_symbol_count_mapping[sentence_attribute.sentence_index] = 0
            else:
                reduce_symbol_count_mapping[sentence_attribute.sentence_index] = len(sentence) - 1
            non_terminal: str = sentence[0]
            self._reduce_non_terminal_index.append(self._non_terminal_index_mapping[non_terminal])
            reduce_non_terminal_index_mapping[sentence_attribute.sentence_index] = self._non_terminal_index_mapping[non_terminal]
            self._non_terminal_sentence_index_mapping.setdefault(non_terminal, set())
            self._non_terminal_sentence_index_mapping[non_terminal].add(sentence_attribute.sentence_index)
            self._index_sentence_mapping[sentence_attribute.sentence_index] = sentence
        self._reduce_non_terminal_index: List[int] = [index for _, index in sorted(reduce_non_terminal_index_mapping.items())]
        self._reduce_symbol_count: List[int] = [count for _, count in sorted(reduce_symbol_count_mapping.items())]

    def __generate_symbol_set(self) -> None:
        self._non_terminal_set: Set[str] = {sentence[0] for sentence in self._sentence_set}
        self._non_terminal_index_mapping: Dict[str, int] = {}
        index_number: int = 0
        for symbol in self._non_terminal_set:
            self._non_terminal_index_mapping[symbol] = index_number
            index_number += 1
        right_symbol_set = set()
        for sentence in self._sentence_set:
            right_symbol_set |= set(sentence)
        self._terminal_set = right_symbol_set - self._non_terminal_set - {configure.boson_null_symbol} | {configure.boson_end_symbol}
        self._terminal_index_mapping = {}
        index_number: int = 0
        for symbol in self._terminal_set:
            self._terminal_index_mapping[symbol] = index_number
            index_number += 1

    def _sentence_first_set(self, sentence: Tuple[str, ...]) -> Set[str]:
        sentence_first_set: Set[str] = set()
        for symbol in sentence:
            if symbol in self._non_terminal_set:
                symbol_first_set: Set[str] = self._first_set_mapping.get(symbol, set())
                sentence_first_set |= symbol_first_set - {configure.boson_null_symbol}
                if configure.boson_null_symbol not in symbol_first_set:
                    break
            else:
                sentence_first_set.add(symbol)
                break
        else:
            sentence_first_set.add(configure.boson_null_symbol)
        return sentence_first_set

    def _generate_non_terminal_first_set(self) -> None:
        self._first_set_mapping: Dict[str, Set[str]] = {}
        old_set_size: Dict[str, int] = {}
        continue_loop: bool = True
        while continue_loop:
            continue_loop: bool = False
            for sentence in self._sentence_set:
                self._first_set_mapping.setdefault(sentence[0], set())
                self._first_set_mapping[sentence[0]] |= self._sentence_first_set(sentence[1:])
            for non_terminal in self._non_terminal_set:
                if len(self._first_set_mapping[non_terminal]) != old_set_size.get(non_terminal, 0):
                    old_set_size[non_terminal] = len(self._first_set_mapping[non_terminal])
                    continue_loop: bool = True

    def _generate_non_terminal_follow_set(self) -> None:
        self._follow_set_mapping: Dict[str, Set[str]] = {configure.boson_augmented_start: {configure.boson_end_symbol}}
        old_set_size: Dict[str, int] = {}
        continue_loop: bool = True
        while continue_loop:
            continue_loop: bool = False
            for sentence in self._sentence_set:
                self._follow_set_mapping.setdefault(sentence[0], set())
                scan_index: int = 1
                while scan_index < len(sentence):
                    current_symbol: str = sentence[scan_index]
                    if current_symbol in self._non_terminal_set:
                        self._follow_set_mapping.setdefault(current_symbol, set())
                        follow_set: Set[str] = self._sentence_first_set(sentence[scan_index + 1:])
                        self._follow_set_mapping[current_symbol] |= follow_set - {configure.boson_null_symbol}
                        if configure.boson_null_symbol in follow_set:
                            self._follow_set_mapping[current_symbol] |= self._follow_set_mapping[sentence[0]]
                    scan_index += 1
            for non_terminal in self._non_terminal_set:
                if len(self._follow_set_mapping[non_terminal]) != old_set_size.get(non_terminal, 0):
                    old_set_size[non_terminal] = len(self._follow_set_mapping[non_terminal])
                    continue_loop: bool = True

    def sentence_set(self) -> Set[Tuple[str, ...]]:
        return self._sentence_set

    def non_terminal_set(self) -> Set[str]:
        return self._non_terminal_set

    def terminal_set(self) -> Set[str]:
        return self._terminal_set

    def terminal_index_mapping(self) -> Dict[str, int]:
        return self._terminal_index_mapping

    def reduce_symbol_count(self) -> List[int]:
        return self._reduce_symbol_count

    def reduce_non_terminal_index(self) -> List[int]:
        return self._reduce_non_terminal_index

    def sentence_index_grammar_tuple_mapping(self) -> Dict[int, Tuple[str, ...]]:
        return self._sentence_index_grammar_tuple_mapping

    def none_grammar_tuple_sentence_index_set(self) -> Set[int]:
        return self._none_grammar_tuple_sentence_index_set

    def reduce_number_grammar_name_mapping(self) -> Dict[int, str]:
        return self._reduce_number_grammar_name_mapping

    def naive_reduce_number_set(self) -> Set[int]:
        return self._naive_reduce_number_set

    def initialize(self) -> None:
        self.__augment_grammar()
        self.__generate_symbol_set()
        self.__normalize_sentence()

    def assemble_grammar_tuple(self, sentence_grammar_tuple_mapping: Dict[Tuple[str, ...], Tuple[str | tuple, ...]]) -> None:
        logger.info('[Parser Generator] Assemble Grammar Tuple.')
        self._sentence_index_grammar_tuple_mapping: Dict[int, Tuple[str | tuple, ...]] = {}
        self._grammar_tuple_naive_sentence_set: Set[Tuple[str, ...]] = set()
        sentence_grammar_tuple_list: List[Tuple[Tuple[str, ...], Tuple[str | tuple, ...]]] = list(sentence_grammar_tuple_mapping.items())
        while sentence_grammar_tuple_list:
            sentence, grammar_tuple = sentence_grammar_tuple_list.pop()
            new_grammar_tuple: List[str] = []
            for grammar_node in grammar_tuple:
                if isinstance(grammar_node, tuple):
                    locator: str = grammar_node[0]
                    sub_grammar_tuple: tuple = grammar_node[1]
                else:
                    locator: str = grammar_node
                    sub_grammar_tuple: None = None
                if locator.startswith(configure.boson_grammar_tuple_unpack):
                    if locator == configure.boson_grammar_tuple_unpack:
                        self._grammar_tuple_naive_sentence_set.add(sentence)
                        continue
                    else:
                        index: int = int(locator[1:])
                        unpack: bool = True
                else:
                    index: int = int(locator)
                    unpack: bool = False
                if index >= len(sentence) - 1:
                    raise ValueError('[Parser Generator] Grammar Node Out Of Range.')
                if unpack and sentence[index + 1] not in self._non_terminal_set:
                    raise ValueError('[Parser Generator] Terminal Symbol Can Not Unpack.')
                if sub_grammar_tuple:
                    hidden_name: str = sentence[index + 1]
                    if sub_grammar_tuple[0] == configure.boson_grammar_tuple_unpack:
                        sub_grammar_tuple: tuple = sub_grammar_tuple[1:]
                        unpack_node: bool = True
                    else:
                        unpack_node: bool = False
                    if hidden_name.startswith(configure.boson_operator_name_prefix):
                        for sentence_index in self._non_terminal_sentence_index_mapping[hidden_name]:
                            sub_sentence: Tuple[str, ...] = self._index_sentence_mapping[sentence_index]
                            final_name: str = sub_sentence[-1]
                            if final_name.startswith(configure.boson_hidden_name_prefix):
                                if unpack_node:
                                    origin_tuple: tuple = sentence_grammar_tuple_mapping.get(sub_sentence, ('0',))
                                    origin_tuple: tuple = origin_tuple[:-1] + ('{}{}'.format(configure.boson_grammar_tuple_unpack, origin_tuple[-1]),)
                                    sentence_grammar_tuple_list.insert(0, (sub_sentence, origin_tuple))
                                for final_sentence_index in self._non_terminal_sentence_index_mapping[final_name]:
                                    sentence_grammar_tuple_list.append((self._index_sentence_mapping[final_sentence_index], sub_grammar_tuple))
                                if not unpack_node:
                                    break
                        else:
                            if not unpack_node:
                                raise ValueError('[Parser Generator] Symbol Closure Can Not Use Grammar Tuple.')
                    elif hidden_name.startswith(configure.boson_hidden_name_prefix):
                        for sentence_index in self._non_terminal_sentence_index_mapping[hidden_name]:
                            sentence_grammar_tuple_list.append((self._index_sentence_mapping[sentence_index], sub_grammar_tuple))
                    else:
                        raise ValueError('[Parser Generator] Symbol Can Not Use Grammar Tuple.')
                new_grammar_tuple.append((configure.boson_grammar_tuple_unpack if unpack else '') + str(index))
            sentence_attribute: SentenceAttribute = self._sentence_attribute_mapping[sentence]
            self._sentence_index_grammar_tuple_mapping[sentence_attribute.sentence_index] = tuple(new_grammar_tuple)
        self._none_grammar_tuple_sentence_index_set: Set[int] = set(range(len(self._sentence_set))) - set(self._sentence_index_grammar_tuple_mapping)

    def assemble_sentence_grammar_name(self, sentence_grammar_name_mapping: Dict[Tuple[str, ...], str]) -> None:
        logger.info('[Parser Generator] Assemble Sentence Grammar Name.')
        self._reduce_number_grammar_name_mapping: Dict[int, str] = {}
        for sentence, grammar_name in sentence_grammar_name_mapping.items():
            sentence_attribute: SentenceAttribute = self._sentence_attribute_mapping[sentence]
            self._reduce_number_grammar_name_mapping[sentence_attribute.sentence_index] = grammar_name

    def assemble_naive_sentence(self, naive_sentence_set: Set[Tuple[str, ...]]) -> None:
        logger.info('[Parser Generator] Assemble Naive Sentence.')
        self._naive_reduce_number_set: Set[int] = set()
        for sentence in naive_sentence_set | self._grammar_tuple_naive_sentence_set:
            sentence_attribute: SentenceAttribute = self._sentence_attribute_mapping[sentence]
            self._naive_reduce_number_set.add(sentence_attribute.sentence_index)
