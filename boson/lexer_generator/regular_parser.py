class RegularToken:
    text: str
    line: int
    symbol: str

    def __init__(self, text: str, line: int, symbol: str):
        self.text = text
        self.line = line
        self.symbol = symbol


class RegularLexer:
    def __init__(self):
        self.__token_list: list = []
        self.__line: int = 1
        self.__error_line: int = -1
        self.__no_error_line: int = -1
        self.__skip: bool = False
        self.__move_table: dict = {
            0: [
                [0, set(), [('0', '9')], 1],
                [2, {'?'}, [('(', '.'), ('0', '9'), ('[', '^'), ('{', '}')], 2],
                [0, {'|'}, [], 3],
                [0, {'.'}, [], 4],
                [0, {'['}, [], 5],
                [0, {'^'}, [], 6],
                [0, {'\\'}, [], 7],
                [0, {']'}, [], 8],
                [0, {'('}, [], 9],
                [0, {')'}, [], 10],
                [0, {'{'}, [], 11],
                [0, {'-'}, [], 12],
                [0, {'+'}, [], 13],
                [0, {'*'}, [], 14],
                [0, {'?'}, [], 15],
                [0, {','}, [], 16],
                [0, {'}'}, [], 17]
            ],
            11: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 18]
            ],
            18: [
                [0, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 18],
                [0, {'}'}, [], 19]
            ],
            7: [
                [2, set(), [], 20]
            ]
        }
        self.__character_set: set = {'H', 'J', '}', 'R', '9', 'L', 'Q', ']', '8', '-', 'T', '{', 't', 'K', 'X', 'a', 'Z', '|', 'z', '6', 'p', '[', 'd', 'n', 'm', '_', '*', 'G', 'F', '^', '.', 'V', 'b', '7', 'O', 'W', 'o', '5', 'y', 's', 'S', 'P', 'M', '2', 'c', 'B', 'v', 'r', 'A', '?', 'E', '1', 'e', 'Y', '+', 'f', 'u', 'I', ',', '3', 'w', 'g', 'D', 'q', 'i', 'k', 'N', 'j', '\\', 'U', '(', '0', 'h', 'x', 'l', 'C', '4', ')'}
        self.__start_state: int = 0
        self.__end_state_set: set = {1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20}
        self.__lexical_symbol_mapping: dict = {
            1: 'single_number',
            2: 'normal_character',
            3: '!symbol_1',
            4: '!symbol_2',
            5: '!symbol_3',
            6: '!symbol_4',
            8: '!symbol_5',
            9: '!symbol_6',
            10: '!symbol_7',
            11: '!symbol_12',
            12: '!symbol_8',
            13: '!symbol_9',
            14: '!symbol_10',
            15: '!symbol_11',
            16: '!symbol_13',
            17: '!symbol_14',
            19: 'reference',
            20: 'escape_character'
        }
        self.__non_greedy_state_set: set = set()
        self.__symbol_function_mapping: dict = {
            'single_number': [],
            'escape_character': [],
            'reference': ['reference'],
            'normal_character': []
        }
        self.__lexical_function: dict = {}

    def _invoke_lexical_function(self, symbol: str, token_string: str) -> str:
        self.__skip = False
        if symbol in self.__symbol_function_mapping:
            for function in self.__symbol_function_mapping[symbol]:
                if function in self.__lexical_function:
                    token_string = self.__lexical_function[function](token_string)
                elif function == 'skip':
                    self.skip()
                elif function == 'newline':
                    self.newline()
        return token_string

    def _generate_token(self, state: int, token_string: str) -> None:
        symbol = self.__lexical_symbol_mapping.get(state, '!symbol')
        token_string = self._invoke_lexical_function(symbol, token_string)
        if not self.__skip:
            self.__token_list.append(RegularToken(token_string, self.__line, symbol))

    def skip(self) -> None:
        self.__skip = True

    def newline(self) -> None:
        self.__line += 1

    def token_list(self) -> list:
        return self.__token_list

    def error_line(self) -> int:
        return self.__error_line

    def no_error_line(self) -> int:
        return self.__no_error_line

    def tokenize(self, text: str) -> int:
        self.__token_list = []
        self.__error_line = self.__no_error_line
        self.__line = 1
        state = self.__start_state
        token_string = ''
        index = 0
        while index < len(text):
            character = text[index]
            index += 1
            get_token = False
            if state in self.__non_greedy_state_set:
                get_token = True
            if not get_token and state in self.__move_table:
                for attribute, character_set, range_list, next_state in self.__move_table[state]:
                    if attribute == 2:
                        condition = character not in character_set
                        for min_character, max_character in range_list:
                            condition &= character < min_character or character > max_character
                    else:
                        condition = character in character_set
                        if attribute == 1 and character not in self.__character_set:
                            condition = True
                        for min_character, max_character in range_list:
                            if condition or min_character <= character <= max_character:
                                condition = True
                                break
                    if condition:
                        token_string += character
                        state = next_state
                        break
                else:
                    if state in self.__end_state_set:
                        get_token = True
                    else:
                        self.__error_line = self.__line
                        return self.__error_line
            else:
                if get_token or state in self.__end_state_set:
                    get_token = True
                else:
                    raise ValueError('Invalid state: state={}'.format(state))
            if get_token:
                self._generate_token(state, token_string)
                token_string = ''
                state = self.__start_state
                index -= 1
        if state in self.__end_state_set:
            self._generate_token(state, token_string)
        else:
            raise ValueError('Invalid state: state={}'.format(state))
        self.__token_list.append(RegularToken('', self.__line, '$'))
        return self.__error_line

    def register_function(self, function_name: str) -> callable:
        def decorator(f: callable):
            self.__lexical_function[function_name] = f
            return f
        return decorator


class BosonGrammarNode:
    def __init__(self):
        self.reduce_number = -1
        self.__data: list = []

    def __getitem__(self, item):
        return self.__data[item]

    def __iadd__(self, other):
        self.__data += other
        return self

    def append(self, item) -> None:
        self.__data.append(item)

    def insert(self, index, item) -> None:
        self.__data.insert(index, item)

    def data(self) -> list:
        return self.__data


class BosonGrammar:
    def __init__(self):
        self.__grammar_tree: (BosonGrammarNode, None) = None
        self.__error_index: int = -1
        self.__no_error_index: int = -1

    def get_grammar_tree(self) -> (BosonGrammarNode, None):
        return self.__grammar_tree

    def set_grammar_tree(self, grammar_tree: BosonGrammarNode) -> None:
        self.__grammar_tree = grammar_tree

    grammar_tree = property(get_grammar_tree, set_grammar_tree)

    def get_error_index(self) -> int:
        return self.__error_index

    def set_error_index(self, error_index: int) -> None:
        self.__error_index = error_index

    error_index = property(get_error_index, set_error_index)

    def no_error_index(self) -> int:
        return self.__no_error_index


class RegularParser:
    def __init__(self):
        self.__terminal_index_mapping: dict = {
            'reference': 0,
            '!symbol_14': 1,
            '!symbol_9': 2,
            '!symbol_5': 3,
            '!symbol_10': 4,
            '!symbol_3': 5,
            '!symbol_6': 6,
            '!symbol_12': 7,
            '!symbol_1': 8,
            '!symbol_2': 9,
            'escape_character': 10,
            '!symbol_7': 11,
            '!symbol_8': 12,
            '!symbol_13': 13,
            '!symbol_4': 14,
            '!symbol_11': 15,
            'single_number': 16,
            '$': 17,
            'normal_character': 18
        }
        self.__sparse_action_table: dict = {
            0: {0: 's13', 5: 's11', 6: 's12', 9: 's8', 10: 's10', 16: 's15', 18: 's16'},
            1: {17: 'a'},
            2: {17: 'r15'},
            3: {8: 'r7', 11: 'r7', 17: 'r7'},
            4: {0: 's13', 5: 's11', 6: 's12', 8: 'r12', 9: 's8', 10: 's10', 11: 'r12', 16: 's15', 17: 'r12', 18: 's16'},
            5: {0: 'r42', 5: 'r42', 6: 'r42', 8: 'r42', 9: 'r42', 10: 'r42', 11: 'r42', 16: 'r42', 17: 'r42', 18: 'r42'},
            6: {0: 'r36', 2: 's34', 4: 's33', 5: 'r36', 6: 'r36', 7: 's36', 8: 'r36', 9: 'r36', 10: 'r36', 11: 'r36', 15: 's35', 16: 'r36', 17: 'r36', 18: 'r36'},
            7: {0: 'r1', 2: 'r1', 4: 'r1', 5: 'r1', 6: 'r1', 7: 'r1', 8: 'r1', 9: 'r1', 10: 'r1', 11: 'r1', 15: 'r1', 16: 'r1', 17: 'r1', 18: 'r1'},
            8: {0: 'r28', 2: 'r28', 4: 'r28', 5: 'r28', 6: 'r28', 7: 'r28', 8: 'r28', 9: 'r28', 10: 'r28', 11: 'r28', 15: 'r28', 16: 'r28', 17: 'r28', 18: 'r28'},
            9: {0: 'r29', 2: 'r29', 4: 'r29', 5: 'r29', 6: 'r29', 7: 'r29', 8: 'r29', 9: 'r29', 10: 'r29', 11: 'r29', 15: 'r29', 16: 'r29', 17: 'r29', 18: 'r29'},
            10: {0: 'r24', 2: 'r24', 3: 'r24', 4: 'r24', 5: 'r24', 6: 'r24', 7: 'r24', 8: 'r24', 9: 'r24', 10: 'r24', 11: 'r24', 15: 'r24', 16: 'r24', 17: 'r24', 18: 'r24'},
            11: {10: 'r11', 14: 's19', 16: 'r11', 18: 'r11'},
            12: {0: 's13', 5: 's11', 6: 's12', 9: 's8', 10: 's10', 16: 's15', 18: 's16'},
            13: {0: 'r20', 2: 'r20', 4: 'r20', 5: 'r20', 6: 'r20', 7: 'r20', 8: 'r20', 9: 'r20', 10: 'r20', 11: 'r20', 15: 'r20', 16: 'r20', 17: 'r20', 18: 'r20'},
            14: {0: 'r34', 2: 'r34', 4: 'r34', 5: 'r34', 6: 'r34', 7: 'r34', 8: 'r34', 9: 'r34', 10: 'r34', 11: 'r34', 15: 'r34', 16: 'r34', 17: 'r34', 18: 'r34'},
            15: {0: 'r23', 2: 'r23', 3: 'r23', 4: 'r23', 5: 'r23', 6: 'r23', 7: 'r23', 8: 'r23', 9: 'r23', 10: 'r23', 11: 'r23', 12: 'r23', 15: 'r23', 16: 'r23', 17: 'r23', 18: 'r23'},
            16: {0: 'r26', 2: 'r26', 3: 'r26', 4: 'r26', 5: 'r26', 6: 'r26', 7: 'r26', 8: 'r26', 9: 'r26', 10: 'r26', 11: 'r26', 12: 'r26', 15: 'r26', 16: 'r26', 17: 'r26', 18: 'r26'},
            17: {11: 's18'},
            18: {0: 'r13', 2: 'r13', 4: 'r13', 5: 'r13', 6: 'r13', 7: 'r13', 8: 'r13', 9: 'r13', 10: 'r13', 11: 'r13', 15: 'r13', 16: 'r13', 17: 'r13', 18: 'r13'},
            19: {10: 'r14', 16: 'r14', 18: 'r14'},
            20: {10: 's10', 16: 's15', 18: 's16'},
            21: {10: 'r8', 16: 'r8', 18: 'r8'},
            22: {3: 'r10', 10: 'r10', 16: 'r10', 18: 'r10'},
            23: {3: 's28', 10: 's10', 16: 's15', 18: 's16'},
            24: {3: 'r37', 10: 'r37', 16: 'r37', 18: 'r37'},
            25: {3: 'r34', 10: 'r34', 12: 's26', 16: 'r34', 18: 'r34'},
            26: {16: 's15', 18: 's16'},
            27: {3: 'r41', 10: 'r41', 16: 'r41', 18: 'r41'},
            28: {0: 'r5', 2: 'r5', 4: 'r5', 5: 'r5', 6: 'r5', 7: 'r5', 8: 'r5', 9: 'r5', 10: 'r5', 11: 'r5', 15: 'r5', 16: 'r5', 17: 'r5', 18: 'r5'},
            29: {3: 'r21', 10: 'r21', 16: 'r21', 18: 'r21'},
            30: {0: 'r2', 5: 'r2', 6: 'r2', 8: 'r2', 9: 'r2', 10: 'r2', 11: 'r2', 16: 'r2', 17: 'r2', 18: 'r2'},
            31: {0: 'r22', 5: 'r22', 6: 'r22', 8: 'r22', 9: 'r22', 10: 'r22', 11: 'r22', 16: 'r22', 17: 'r22', 18: 'r22'},
            32: {0: 'r32', 5: 'r32', 6: 'r32', 8: 'r32', 9: 'r32', 10: 'r32', 11: 'r32', 16: 'r32', 17: 'r32', 18: 'r32'},
            33: {0: 'r6', 5: 'r6', 6: 'r6', 8: 'r6', 9: 'r6', 10: 'r6', 11: 'r6', 16: 'r6', 17: 'r6', 18: 'r6'},
            34: {0: 'r16', 5: 'r16', 6: 'r16', 8: 'r16', 9: 'r16', 10: 'r16', 11: 'r16', 16: 'r16', 17: 'r16', 18: 'r16'},
            35: {0: 'r17', 5: 'r17', 6: 'r17', 8: 'r17', 9: 'r17', 10: 'r17', 11: 'r17', 16: 'r17', 17: 'r17', 18: 'r17'},
            36: {13: 'r27', 16: 's38'},
            37: {1: 'r19', 13: 'r19', 16: 's47'},
            38: {1: 'r9', 13: 'r9', 16: 'r9'},
            39: {13: 's42'},
            40: {13: 'r39'},
            41: {13: 'r40'},
            42: {1: 'r35', 16: 's38'},
            43: {1: 's46'},
            44: {1: 'r4'},
            45: {1: 'r25'},
            46: {0: 'r30', 5: 'r30', 6: 'r30', 8: 'r30', 9: 'r30', 10: 'r30', 11: 'r30', 16: 'r30', 17: 'r30', 18: 'r30'},
            47: {1: 'r3', 13: 'r3', 16: 'r3'},
            48: {0: 'r33', 5: 'r33', 6: 'r33', 8: 'r33', 9: 'r33', 10: 'r33', 11: 'r33', 16: 'r33', 17: 'r33', 18: 'r33'},
            49: {8: 's51', 11: 'r38', 17: 'r38'},
            50: {8: 'r31', 11: 'r31', 17: 'r31'},
            51: {0: 's13', 5: 's11', 6: 's12', 9: 's8', 10: 's10', 16: 's15', 18: 's16'},
            52: {8: 'r18', 11: 'r18', 17: 'r18'}
        }
        self.__sparse_goto_table: dict = {
            0: {5: 2, 9: 5, 10: 14, 11: 6, 13: 9, 17: 1, 18: 4, 19: 7, 23: 3},
            3: {2: 49},
            4: {9: 48, 10: 14, 11: 6, 13: 9, 19: 7},
            6: {12: 31, 14: 30, 24: 32},
            11: {6: 21, 8: 20},
            12: {5: 17, 9: 5, 10: 14, 11: 6, 13: 9, 18: 4, 19: 7, 23: 3},
            20: {1: 22, 3: 23, 10: 25, 19: 24},
            23: {1: 29, 10: 25, 19: 24},
            26: {10: 27},
            36: {4: 37, 7: 40, 15: 41, 21: 39},
            42: {0: 43, 4: 37, 15: 45, 16: 44},
            49: {20: 50},
            51: {9: 5, 10: 14, 11: 6, 13: 9, 18: 4, 19: 7, 23: 52}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            19: ('*0',),
            3: ('*0', '1'),
            30: ('*1', '*3'),
            25: ('0',),
            40: ('0',),
            35: (),
            4: ('*0',),
            27: (),
            39: ('*0',),
            41: ('0', '2'),
            20: ('0',),
            13: ('1',),
            5: ('*1', '2'),
            14: ('0',),
            21: ('*0', '1'),
            11: (),
            8: ('*0',),
            28: ('0',),
            29: ('0',),
            1: ('0',),
            2: ('0', '*1'),
            32: ('0',),
            36: (),
            22: ('*0',),
            12: ('*0',),
            33: ('*0', '1'),
            38: ('0', '*1'),
            18: ('1',),
            7: (),
            31: ('*0', '*1'),
            15: ('0',)
        }
        self.__reduce_symbol_count: list = [1, 1, 2, 2, 1, 4, 1, 0, 1, 1, 1, 0, 1, 3, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 5, 2, 1, 2, 1, 0, 0, 1, 2, 1, 1, 3, 1]
        self.__reduce_non_terminal_index: list = [22, 11, 9, 4, 0, 13, 24, 2, 8, 4, 3, 8, 23, 13, 6, 17, 24, 24, 20, 15, 13, 3, 14, 10, 19, 16, 10, 21, 11, 11, 24, 2, 12, 18, 19, 0, 14, 1, 5, 21, 7, 1, 18]

    def parse(self, token_list: list) -> BosonGrammar:
        grammar = BosonGrammar()
        analysis_stack = [0]
        symbol_stack = []
        token_index = 0
        while token_index < len(token_list):
            token = token_list[token_index]
            current_state = analysis_stack[-1]
            operation = self.__sparse_action_table.get(current_state, {}).get(self.__terminal_index_mapping[token.symbol], 'e')
            operation_flag = operation[0]
            if operation_flag == 'e':
                grammar.error_index = token_index
                return grammar
            elif operation_flag == 's':
                state_number = int(operation[1:])
                analysis_stack.append(state_number)
                token_index += 1
                symbol_stack.append(token.text)
            elif operation_flag == 'r':
                statement_index = int(operation[1:])
                reduce_count = self.__reduce_symbol_count[statement_index]
                for _ in range(reduce_count):
                    analysis_stack.pop()
                current_state = analysis_stack[-1]
                current_non_terminal_index = self.__reduce_non_terminal_index[statement_index]
                goto_next_state = self.__sparse_goto_table.get(current_state, {}).get(current_non_terminal_index, -1)
                if goto_next_state == -1:
                    raise ValueError('Invalid goto action: state={}, non-terminal={}'.format(current_state, current_non_terminal_index))
                analysis_stack.append(goto_next_state)
                if statement_index in self.__sentence_index_grammar_tuple_mapping:
                    symbol_package = []
                    for _ in range(reduce_count):
                        symbol_package.insert(0, symbol_stack.pop())
                    grammar_node = BosonGrammarNode()
                    for node in self.__sentence_index_grammar_tuple_mapping[statement_index]:
                        if node[0] == '*':
                            grammar_node += symbol_package[int(node[1:])]
                        else:
                            grammar_node.append(symbol_package[int(node)])
                    grammar_node.reduce_number = statement_index
                    symbol_stack.append(grammar_node)
                elif statement_index in {0, 34, 37, 6, 9, 10, 42, 16, 17, 23, 24, 26}:
                    grammar_node = BosonGrammarNode()
                    for _ in range(reduce_count):
                        grammar_node.insert(0, symbol_stack.pop())
                    grammar_node.reduce_number = statement_index
                    symbol_stack.append(grammar_node)
                else:
                    raise ValueError('Invalid reduce number: reduce={}'.format(statement_index))
            elif operation_flag == 'a':
                grammar.grammar_tree = symbol_stack[0]
                return grammar
            else:
                raise ValueError('Invalid action: action={}'.format(operation))
        raise RuntimeError('Analyzer unusual exit.')


class RegularInterpreter:
    def __init__(self):
        self.__reduce_number_grammar_name_mapping: dict = {
            15: 'regular_expression',
            38: 'expression',
            12: 'branch',
            2: 'group',
            1: 'simple_construct',
            29: 'complex_construct',
            28: 'wildcard_character',
            5: 'select',
            13: 'sub_expression',
            20: 'reference',
            30: 'count_range',
            19: 'construct_number'
        }
        self.__naive_reduce_number_set: set = {1, 34, 37, 6, 15, 16, 17, 20, 23, 24, 26, 28, 29}
        self.__semantic_action_mapping: dict = {}

    def __semantic_analysis(self, grammar_tree: BosonGrammarNode):
        if grammar_tree.reduce_number in self.__reduce_number_grammar_name_mapping:
            grammar_name = self.__reduce_number_grammar_name_mapping[grammar_tree.reduce_number]
        else:
            grammar_name = '!grammar_hidden'
        semantic_node_list = []
        for grammar_node in grammar_tree.data():
            if isinstance(grammar_node, BosonGrammarNode):
                semantic_node = self.__semantic_analysis(grammar_node)
            else:
                semantic_node = grammar_node
            semantic_node_list.append(semantic_node)
        if grammar_name in self.__semantic_action_mapping:
            return self.__semantic_action_mapping[grammar_name](semantic_node_list)
        elif grammar_tree.reduce_number in self.__naive_reduce_number_set:
            if len(semantic_node_list) == 0:
                return None
            elif len(semantic_node_list) == 1:
                return semantic_node_list[0]
            else:
                return semantic_node_list
        else:
            return semantic_node_list

    def execute(self, grammar_tree: BosonGrammarNode):
        return self.__semantic_analysis(grammar_tree)

    def register_action(self, name: str) -> callable:
        def decorator(f: callable):
            self.__semantic_action_mapping[name] = f
            return f
        return decorator
