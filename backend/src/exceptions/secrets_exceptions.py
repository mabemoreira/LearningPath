class UndefinedSecretException(Exception):
    def __init__(self, details="Undefined secrets were found!"):
        super().__init__(details)
        self.details = details

    def __str__(self):
        return f"{self.__class__.__name__}: {self.details}"
