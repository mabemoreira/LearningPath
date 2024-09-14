import os

from src.exceptions.secrets_exceptions import UndefinedSecretException


class Secrets:
    def __init__(self):
        self.execution_environment: str = os.getenv("EXECUTION_ENVIRONMENT")
        self.django_secret_key: str     = os.getenv("DJANGO_SECRET_KEY")

        self.test_environment = False
        if (
            self.execution_environment is None
            or "main" not in self.execution_environment.lower()
        ):
            self.test_environment = True

    def validate_secrets(self):
        if self.test_environment:
            print("Executing application in TEST environment!")
            print("Ignoring secrets exception!")
            return

        print("Executing application in MAIN environment!")

        undefined_secrets = []
        for secret in self.__dict__:
            if self.__dict__.get(secret) is None:
                undefined_secrets.append(secret)

        if len(undefined_secrets) > 0:
            print("ERROR: Secrets were not defined")
            print("\n".join(undefined_secrets))
            print("-----------------------------------")
            raise UndefinedSecretException


secrets = Secrets()
