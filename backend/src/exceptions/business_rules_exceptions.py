from django.core.exceptions import ObjectDoesNotExist


class DomainDoesNotExist(ObjectDoesNotExist):
    def __init__(self, details="Undefined domain was found!"):
        super().__init__(details)
        self.details = details

    def __str__(self):
        return f"{self.__class__.__name__}: {self.details}"
