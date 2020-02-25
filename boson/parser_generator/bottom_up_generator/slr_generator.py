from boson.parser_generator.bottom_up_generator import BottomUpCanonicalParserGenerator
import boson.configure as configure


class SLRParserGenerator(BottomUpCanonicalParserGenerator):
    def __init__(self, sentence_set: set):
        super().__init__(sentence_set)

    def initialize(self):
        super().initialize()
        self._generate_non_terminal_follow_set()

    def initialize_start_state(self):
        first_flag_sentence_list = []
        for sentence in self._non_terminal_closure[configure.boson_augmented_start]:
            flag = 2 if sentence[-1] == configure.boson_null_symbol else 1
            first_flag_sentence_list.append(((sentence, frozenset(self._follow_set_mapping[sentence[0]])), flag))
        return first_flag_sentence_list

    def sentence_look_ahead_set(self, sentence: tuple) -> (frozenset, None):
        return frozenset(self._follow_set_mapping[sentence[0]])

    def state_post_processing(self, state: set) -> set:
        return state
