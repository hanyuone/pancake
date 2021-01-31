class Reader:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def next(self):
        if self.position == len(self.tokens):
            return self.tokens[-1]

        self.position += 1
        return self.tokens[self.position - 1]

    def peek(self):
        return self.tokens[self.position]
