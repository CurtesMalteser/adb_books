class InvalidRequestError(Exception):
    def __init__(self, code, message):
        self.message = message
        self.code = code
        super().__init__(self.message)