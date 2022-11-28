import parser

class RuntimeE(RuntimeError):
    def __init__(self, token, message):
        super().__init__(message)
        self.token=token

class Return(RuntimeE):
    def __init__(self, value):
        super().__init__(None, None)
        self.value=value