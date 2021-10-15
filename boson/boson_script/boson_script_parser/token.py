class LexicalToken:
    text: str
    line: int
    symbol: str

    def __init__(self, text: str, line: int, symbol: str):
        self.text: str = text
        self.line: int = line
        self.symbol: str = symbol
