class AnalyzerTable:
    def __init__(self):
        self.terminal_index = None
        self.action_table = None
        self.goto_table = None
        self.reduce_symbol_sum = None
        self.reduce_to_non_terminal_index = None
        self.sentence_list = None


class GrammarPackage:
    def __init__(self):
        self.command_list = None
        self.sentence_set = None
        self.grammar_tuple_map = None
        self.none_grammar_tuple_set = None
        self.literal_map = None
        self.literal_reverse_map = None
