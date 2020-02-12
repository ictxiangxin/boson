class AnalyzerTable:
    def __init__(self):
        self.terminal_index = None
        self.action_table = None
        self.goto_table = None
        self.reduce_symbol_sum = None
        self.reduce_to_non_terminal_index = None
        self.sentence_list = None
        self.conflict_list = None


class LexicalPackage:
    def __init__(self):
        self.move_table = None
        self.compact_move_table = None
        self.character_set = None
        self.start_state = None
        self.end_state_set = None
        self.lexical_symbol_mapping = None
        self.symbol_function_mapping = None
        self.non_greedy_state_set = None


class GrammarPackage:
    def __init__(self):
        self.command_list = None
        self.lexical_regular_expression_map = None
        self.sentence_set = None
        self.grammar_tuple_map = None
        self.none_grammar_tuple_set = None
        self.literal_map = None
        self.literal_reverse_map = None
        self.sentence_grammar_map = None
        self.naive_sentence = None
