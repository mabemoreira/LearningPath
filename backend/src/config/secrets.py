import os

from src.exceptions.secrets_exceptions import UndefinedSecretException


class Secrets:
    def __init__(self):
        self.database_user: str = os.getenv("DATABASE_USER")
        self.database_pass: str = os.getenv("DATABASE_PASS")
        self.database_host: str = os.getenv("DATABASE_HOST")
        self.database_port: str = os.getenv("DATABASE_PORT")
        self.database_name: str = os.getenv("DATABASE_NAME")
        self.execution_environment: str = os.getenv("EXECUTION_ENVIRONMENT")

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

    @property
    def database_url(self) -> str:
        if self.test_environment:
            return "postgresql://postgres:1234@localhost:5432/postgres"

        return (
            f"postgresql://{self.database_user}:{self.database_pass}"
            "@"
            f"{self.database_host}:{self.database_port}"
            "/"
            f"{self.database_name}"
        )


secrets = Secrets()
